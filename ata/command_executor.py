"""
命令执行模块

负责执行生成的命令并处理结果。
提供安全检查和跨平台支持。
"""

import os
import re
import sys
import shlex
import signal
import logging
import platform
import subprocess
import time
import psutil
from typing import Dict, List, Optional, Tuple, Union
from pathlib import Path
from dataclasses import dataclass

from .config_manager import ConfigManager
from .exceptions import CommandExecutionError, SecurityError

logger = logging.getLogger(__name__)


@dataclass
class CommandResult:
    """命令执行结果"""
    success: bool
    exit_code: int
    stdout: str
    stderr: str
    duration: float


class CommandExecutor:
    """命令执行器类，负责安全地执行命令"""
    
    # 危险命令模式
    DANGEROUS_PATTERNS = [
        r"rm\s+-rf\s+/",  # 删除根目录
        r"rm\s+-rf\s+~",  # 删除用户目录
        r"rm\s+-rf\s+\*",  # 删除所有文件
        r"mkfs",  # 格式化文件系统
        r"dd\s+if=/dev/zero",  # 磁盘写零
        r">\s+/dev/sd[a-z]",  # 直接写入磁盘
        r"chmod\s+-R\s+777",  # 修改权限为777
        r":(){:\|:&};:",  # Fork炸弹
        r"wget\s+.*\s+\|\s+bash",  # 下载并执行脚本
        r"curl\s+.*\s+\|\s+bash",  # 下载并执行脚本
    ]
    
    def __init__(self, config: ConfigManager):
        """初始化命令执行器
        
        Args:
            config: 配置管理器实例
        """
        self.config = config
        
        # 初始化工作目录
        self.working_directory = config.get("general.working_directory")
        if not self.working_directory:
            self.working_directory = str(Path.home())
        
        # 确保工作目录存在
        try:
            os.makedirs(self.working_directory, exist_ok=True)
        except Exception as e:
            logger.error(f"创建工作目录失败: {str(e)}")
            self.working_directory = str(Path.home())
        
        # 初始化系统信息和其他配置
        self.system_info = self._get_system_info()
        self.dangerous_commands = config.get("security.dangerous_commands", [])
        self.sensitive_dirs = config.get("security.sensitive_directories", [])
        self.require_confirmation = config.get("security.require_confirmation", True)
        
        # 设置环境变量
        self.env = os.environ.copy()
        self.env["PYTHONIOENCODING"] = "utf-8"
        
        # Windows系统下设置控制台编码
        if platform.system() == "Windows":
            os.system("chcp 65001")
    
    def _get_system_info(self) -> Dict[str, str]:
        """获取系统信息
        
        Returns:
            系统信息字典
        """
        info = {
            "os": platform.system().lower(),
            "os_version": platform.version(),
            "architecture": platform.machine(),
            "python_version": platform.python_version(),
            "shell": os.environ.get("SHELL", ""),
            "user": os.environ.get("USER", ""),
            "home": str(Path.home()),
            "working_directory": self.working_directory,
        }
        
        # Windows特定信息
        if info["os"] == "windows":
            info["shell"] = os.environ.get("COMSPEC", "cmd.exe")
        
        return info
    
    def _is_dangerous_command(self, command: str) -> Tuple[bool, Optional[str]]:
        """检查命令是否危险
        
        Args:
            command: 要检查的命令
        
        Returns:
            (是否危险, 警告信息)
        """
        warnings = []
        
        # 检查危险命令模式
        for pattern in self.DANGEROUS_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                warnings.append(f"命令匹配危险模式: {pattern}")
        
        # 检查敏感目录
        for dir_path in self.sensitive_dirs:
            if dir_path in command:
                warnings.append(f"命令涉及敏感目录: {dir_path}")
        
        # 检查特权命令
        if command.startswith(("sudo ", "su ")):
            warnings.append("命令需要特权访问")
        
        # 检查管道和重定向到系统目录
        if ">" in command or "|" in command:
            for dir_path in self.sensitive_dirs:
                if dir_path in command:
                    warnings.append(f"命令包含对敏感目录的重定向或管道操作: {dir_path}")
        
        return len(warnings) > 0, warnings
    
    def _parse_command(self, command: str) -> List[str]:
        """解析命令字符串
        
        Args:
            command: 命令字符串
        
        Returns:
            命令参数列表
        
        Raises:
            CommandExecutionError: 命令解析错误
        """
        try:
            if self.system_info["os"] == "windows":
                # Windows命令解析
                return ["cmd.exe", "/c", command]
            else:
                # Unix命令解析
                return shlex.split(command)
        except Exception as e:
            raise CommandExecutionError(f"命令解析错误: {str(e)}")
    
    def execute(
        self,
        command: str,
        timeout: Optional[int] = None,
        capture_output: bool = True,
        check: bool = True,
        env: Optional[Dict[str, str]] = None,
        shell: bool = False,
    ) -> CommandResult:
        """执行命令
        
        Args:
            command: 要执行的命令
            timeout: 超时时间（秒）
            capture_output: 是否捕获输出
            check: 是否检查返回码
            env: 环境变量
            shell: 是否使用shell执行
        
        Returns:
            命令执行结果
        
        Raises:
            CommandExecutionError: 命令执行错误
            SecurityError: 安全检查错误
        """
        logger.info(f"执行命令: {command}")
        
        # 检查命令是否为空
        if not command or not command.strip():
            raise CommandExecutionError("命令不能为空")
        
        # 检查命令是否危险
        is_dangerous, warnings = self._is_dangerous_command(command)
        if is_dangerous:
            if self.require_confirmation:
                raise SecurityError(f"危险命令需要确认: {', '.join(warnings)}")
            else:
                logger.warning(f"执行危险命令: {', '.join(warnings)}")
        
        try:
            # 准备环境变量
            cmd_env = self.env.copy()
            if env:
                cmd_env.update(env)
            
            # 解析命令
            if shell:
                cmd_args = command
            else:
                cmd_args = self._parse_command(command)
            
            # 执行命令
            start_time = time.time()
            
            process = subprocess.run(
                cmd_args,
                cwd=self.working_directory,
                env=cmd_env,
                timeout=timeout,
                capture_output=capture_output,
                text=True,
                shell=shell,
                check=check,
                encoding='utf-8',
                errors='replace'
            )
            
            duration = time.time() - start_time
            
            result = CommandResult(
                success=(process.returncode == 0),
                exit_code=process.returncode,
                stdout=process.stdout if capture_output else "",
                stderr=process.stderr if capture_output else "",
                duration=duration
            )
            
            logger.debug(f"命令执行结果: {result}")
            return result
            
        except subprocess.TimeoutExpired as e:
            raise CommandExecutionError(f"命令执行超时: {str(e)}")
        except subprocess.CalledProcessError as e:
            raise CommandExecutionError(f"命令执行失败: {str(e)}")
        except Exception as e:
            raise CommandExecutionError(f"命令执行错误: {str(e)}")
    
    def execute_background(
        self,
        command: str,
        env: Optional[Dict[str, str]] = None,
        shell: bool = False,
    ) -> subprocess.Popen:
        """在后台执行命令
        
        Args:
            command: 要执行的命令
            env: 环境变量
            shell: 是否使用shell执行
        
        Returns:
            进程对象
        
        Raises:
            CommandExecutionError: 命令执行错误
            SecurityError: 安全检查错误
        """
        # 检查命令是否为空
        if not command or not command.strip():
            raise CommandExecutionError("命令不能为空")
        
        # 检查命令是否危险
        is_dangerous, warnings = self._is_dangerous_command(command)
        if is_dangerous:
            if self.require_confirmation:
                raise SecurityError(f"危险命令需要确认: {', '.join(warnings)}")
            else:
                logger.warning(f"执行危险命令: {', '.join(warnings)}")
        
        try:
            # 准备环境变量
            cmd_env = self.env.copy()
            if env:
                cmd_env.update(env)
            
            # 解析命令
            if shell:
                cmd_args = command
            else:
                cmd_args = self._parse_command(command)
            
            # 执行命令
            process = subprocess.Popen(
                cmd_args,
                cwd=self.working_directory,
                env=cmd_env,
                shell=shell,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            return process
            
        except Exception as e:
            raise CommandExecutionError(f"后台命令执行错误: {str(e)}")
    
    def terminate_process(self, process: subprocess.Popen) -> None:
        """终止进程
        
        Args:
            process: 进程对象
        """
        if process.poll() is None:  # 进程仍在运行
            if self.system_info["os"] == "windows":
                process.terminate()  # Windows
            else:
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)  # Unix
    
    def change_directory(self, path: Union[str, Path]) -> None:
        """更改工作目录
        
        Args:
            path: 目标目录路径
        
        Raises:
            CommandExecutionError: 目录不存在或无法访问
        """
        try:
            path = Path(path).expanduser().resolve()
            os.chdir(path)
            self.working_directory = str(path)
        except Exception as e:
            raise CommandExecutionError(f"无法切换到目录 {path}: {str(e)}")
    
    def get_working_directory(self) -> str:
        """获取当前工作目录
        
        Returns:
            工作目录路径
        """
        return self.working_directory
    
    def get_system_info(self) -> Dict[str, str]:
        """获取系统信息
        
        Returns:
            系统信息字典
        """
        try:
            info = {
                "os": platform.system(),
                "platform": sys.platform,
                "python_version": sys.version,
                "cpu_count": psutil.cpu_count(),
                "memory_total": psutil.virtual_memory().total,
                "disk_usage": psutil.disk_usage('/').percent,
                "working_directory": self.working_directory or os.getcwd()
            }
            logger.debug(f"系统信息: {info}")
            return info
        except Exception as e:
            logger.error(f"获取系统信息失败: {str(e)}", exc_info=True)
            return {}
    
    def is_windows(self) -> bool:
        """检查是否为Windows系统
        
        Returns:
            是否为Windows系统
        """
        return self.system_info["os"] == "windows"

    def is_dangerous(self, command: str) -> Tuple[bool, List[str]]:
        """检查命令是否危险
        
        Args:
            command: 要检查的命令
            
        Returns:
            (是否危险, 警告信息列表)
        """
        is_dangerous, warnings = self._is_dangerous_command(command)
        logger.info(f"命令安全检查 - 命令: {command}, 是否危险: {is_dangerous}, 警告: {warnings}")
        return is_dangerous, warnings

