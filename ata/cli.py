"""
命令行界面模块

负责处理用户输入和显示结果。
提供丰富的交互功能和错误处理。
"""

import os
import sys
import platform
import argparse
import json
import logging
import asyncio
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt, Confirm
from rich.syntax import Syntax
from rich.table import Table
from rich.logging import RichHandler
from rich.live import Live
from rich.spinner import Spinner

from . import __version__
from .ai_interface import AIInterface, Message
from .command_executor import CommandExecutor, CommandResult
from .config_manager import ConfigManager
from .exceptions import ATAError, AIError, APIError, CommandExecutionError, SecurityError, ConfigError

logger = logging.getLogger(__name__)


class CLI:
    """命令行界面类，负责处理用户输入和显示结果"""

    def __init__(self, ai_interface: Optional[AIInterface] = None, 
                 command_executor: Optional[CommandExecutor] = None,
                 config_manager: Optional[ConfigManager] = None):
        """
        初始化命令行界面
        
        参数:
            ai_interface: AI模型接口
            command_executor: 命令执行器
            config_manager: 配置管理器
        """
        self.config_manager = config_manager or ConfigManager()
        
        # 设置日志记录
        self._setup_logging()
        
        # 如果没有提供AI接口，创建一个新的
        if ai_interface is None:
            provider = self.config_manager.get("ai.provider", "openai")
            provider_config = self.config_manager.get_provider_config(provider)
            model = provider_config.get("model")
            
            self.ai_interface = AIInterface(
                provider=provider,
                model=model,
                fallback_provider=self.config_manager.get("ai.fallback_provider"),
                fallback_model=self.config_manager.get_provider_config(
                    self.config_manager.get("ai.fallback_provider")
                ).get("model")
            )
        else:
            self.ai_interface = ai_interface
        
        # 如果没有提供命令执行器，创建一个新的
        if command_executor is None:
            self.command_executor = CommandExecutor(self.config_manager)
        else:
            self.command_executor = command_executor
        
        # 创建Rich控制台
        self.console = Console()
        
        # 加载历史记录
        self.history: List[Dict[str, str]] = self._load_history()
        
        # 调试模式
        self.debug = self.config_manager.get("ui.debug_mode", False)
        
        # 加载欢迎信息
        self.show_welcome = self.config_manager.get("ui.show_welcome", True)
        
        # 加载颜色配置
        self.colors = self.config_manager.get("ui.colors", {
            "success": "green",
            "error": "red",
            "warning": "yellow",
            "info": "blue"
        })
    
    def _setup_logging(self) -> None:
        """设置日志记录"""
        if not self.config_manager.get("logging.enabled", True):
            return
        
        # 创建日志目录
        log_file = Path(self.config_manager.get("logging.file"))
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # 设置日志格式
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        
        # 设置Rich处理器
        rich_handler = RichHandler(
            rich_tracebacks=True,
            markup=True,
            show_time=False,
            console=self.console
        )
        
        # 设置文件处理器
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=self.config_manager.get("logging.max_size", 10) * 1024 * 1024,
            backupCount=self.config_manager.get("logging.backup_count", 5),
            encoding="utf-8"
        )
        
        # 配置日志记录
        logging.basicConfig(
            level=self.config_manager.get("logging.level", "INFO"),
            format=log_format,
            handlers=[rich_handler, file_handler]
        )
        
        self.logger = logging.getLogger("ata")
    
    def _load_history(self) -> List[Dict[str, str]]:
        """加载命令历史记录"""
        history_file = Path(self.config_manager.get("general.command_history_file"))
        
        try:
            if history_file.exists():
                with open(history_file, "r", encoding="utf-8") as f:
                    history = json.load(f)
                return history[-self.config_manager.get("general.history_size", 20):]
        except Exception as e:
            self.logger.warning(f"加载历史记录失败: {e}")
        
        return []
    
    def _save_history(self) -> None:
        """保存命令历史记录"""
        history_file = Path(self.config_manager.get("general.command_history_file"))
        
        try:
            # 确保目录存在
            history_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(history_file, "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.warning(f"保存历史记录失败: {e}")
    
    def _show_welcome(self) -> None:
        """显示欢迎信息"""
        if not self.show_welcome:
            return
        
        welcome_text = """
# AI Terminal Assistant

欢迎使用AI终端助手！我可以帮助你：

- 将自然语言转换为命令行命令
- 解释命令的作用和参数
- 提供命令使用建议和警告
- 自动检测和防范危险操作

当前配置：
- AI提供商: {provider}
- 模型: {model}
- 工作目录: {working_dir}

输入 'help' 查看帮助，输入 'exit' 退出。
        """.format(
            provider=self.config_manager.get("ai.provider"),
            model=self.ai_interface.model,
            working_dir=self.command_executor.working_dir
        )
        
        self.console.print(Panel(Markdown(welcome_text)))
    
    def _show_help(self) -> None:
        """显示帮助信息"""
        help_text = """
# 命令帮助

## 基本命令
- help: 显示此帮助信息
- exit/quit: 退出程序
- clear: 清屏
- history: 显示历史记录

## AI相关命令
- switch <provider>: 切换AI提供商 (openai/deepseek)
- model <name>: 切换AI模型
- temp <value>: 设置温度 (0.0-1.0)

## 系统命令
- cd <path>: 更改工作目录
- pwd: 显示当前工作目录
- debug: 切换调试模式

## 配置命令
- config show: 显示当前配置
- config reset: 重置配置
- config export <path>: 导出配置
- config import <path>: 导入配置

## 提示
- 直接输入自然语言描述你想执行的操作
- 命令执行前会进行安全检查
- 危险操作需要确认
- 使用 Ctrl+C 中断当前操作
        """
        
        self.console.print(Panel(Markdown(help_text)))
    
    async def process_user_input(self, user_input: str) -> bool:
        """处理用户输入
        
        Args:
            user_input: 用户输入的文本
            
        Returns:
            是否继续运行
        """
        # 检查特殊命令
        if user_input.lower() in ('exit', 'quit'):
            return False
        elif user_input.lower() == 'help':
            self._show_help()
            return True
        elif not user_input.strip():
            return True
        
        try:
            # 生成命令
            self.console.print("[bold blue]思考中...[/]")
            command = await self.ai_interface.chat(user_input)
            
            # 显示生成的命令
            self.console.print("\n[bold green]生成的命令:[/]")
            self.console.print(command)
            
            # 检查命令安全性
            is_dangerous, warnings = self.command_executor.is_dangerous(command)
            if is_dangerous:
                self.console.print("\n[bold red]安全警告:[/]")
                for warning in warnings:
                    self.console.print(f"- {warning}")
            
            # 获取用户确认
            while True:
                choice = Prompt.ask(
                    "\n是否执行此命令?",
                    choices=['y', 'n', 'e'],
                    default='n'
                )
                
                if choice == 'y':
                    # 执行命令
                    self.console.print("\n[bold blue]执行命令...[/]")
                    result = self.command_executor.execute(command)
                    
                    # 显示结果
                    self.console.print("\n[bold]执行结果:[/]")
                    if result.success:
                        self.console.print("[green]命令执行成功[/]")
                    else:
                        self.console.print("[red]命令执行失败[/]")
                    
                    if result.stdout:
                        self.console.print("\n[bold]输出:[/]")
                        self.console.print(result.stdout)
                    
                    if result.stderr:
                        self.console.print("\n[bold red]错误:[/]")
                        self.console.print(result.stderr)
                    
                    self.console.print(f"\n退出代码: {result.exit_code}")
                    break
                    
                elif choice == 'e':
                    # 编辑命令
                    self.console.print("\n[bold]原始命令:[/]")
                    self.console.print(command)
                    edited_command = Prompt.ask("编辑命令")
                    
                    if edited_command:
                        self.console.print("\n[bold blue]执行命令...[/]")
                        result = self.command_executor.execute(edited_command)
                        
                        # 显示结果
                        self.console.print("\n[bold]执行结果:[/]")
                        if result.success:
                            self.console.print("[green]命令执行成功[/]")
                        else:
                            self.console.print("[red]命令执行失败[/]")
                        
                        if result.stdout:
                            self.console.print("\n[bold]输出:[/]")
                            self.console.print(result.stdout)
                        
                        if result.stderr:
                            self.console.print("\n[bold red]错误:[/]")
                            self.console.print(result.stderr)
                        
                        self.console.print(f"\n退出代码: {result.exit_code}")
                    break
                    
                elif choice == 'n':
                    self.console.print("已取消执行")
                    break
            
            # 保存到历史记录
            self.history.append({
                "timestamp": datetime.now().isoformat(),
                "input": user_input,
                "response": command,
                "command": command
            })
            self._save_history()
            
            return True
            
        except Exception as e:
            logger.error(f"处理用户输入时出错: {str(e)}", exc_info=True)
            self.console.print(f"[bold red]错误:[/] {str(e)}")
            return True
    
    async def run(self) -> int:
        """运行命令行界面"""
        try:
            self._show_welcome()
            
            while True:
                try:
                    user_input = Prompt.ask("\n请输入命令")
                    should_continue = await self.process_user_input(user_input)
                    if not should_continue:
                        break
                except KeyboardInterrupt:
                    self.console.print("\n程序已中断")
                    return 1
                except Exception as e:
                    logger.error(f"运行CLI时出错: {str(e)}", exc_info=True)
                    self.console.print(f"[bold red]错误:[/] {str(e)}")
                    return 1
            
            return 0
        except Exception as e:
            logger.error(f"运行CLI时出错: {str(e)}", exc_info=True)
            self.console.print(f"[bold red]错误:[/] {str(e)}")
            return 1


def main():
    """主函数"""
    try:
        cli = CLI()
        sys.exit(cli.run())
    except KeyboardInterrupt:
        print("\n程序已中断")
    except Exception as e:
        print(f"\n发生错误: {str(e)}")
        if "--debug" in sys.argv:
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()

