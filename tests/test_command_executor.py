"""
命令执行器测试模块
"""

import os
import platform
import pytest
from pathlib import Path
from typing import Dict, Any

from ata.command_executor import CommandExecutor


@pytest.fixture
def executor() -> CommandExecutor:
    """创建命令执行器实例"""
    return CommandExecutor()


def test_shell_detection(executor: CommandExecutor) -> None:
    """测试shell检测功能"""
    assert executor.shell in ["bash", "zsh", "fish", "powershell", "cmd"]


def test_system_info(executor: CommandExecutor) -> None:
    """测试系统信息获取功能"""
    info = executor.get_system_info()
    assert isinstance(info, dict)
    assert "os" in info
    assert "shell" in info
    assert "working_directory" in info
    assert "python_version" in info
    assert "system_version" in info
    assert "machine" in info


def test_execute_simple_command(executor: CommandExecutor) -> None:
    """测试执行简单命令"""
    # 在Windows上使用不同的命令
    if platform.system().lower() == "windows":
        result = executor.execute("echo Hello")
    else:
        result = executor.execute("echo 'Hello'")
    
    assert result["success"]
    assert "Hello" in result["stdout"]
    assert result["stderr"] == ""
    assert result["exit_code"] == 0
    assert isinstance(result["duration"], float)


def test_execute_invalid_command(executor: CommandExecutor) -> None:
    """测试执行无效命令"""
    result = executor.execute("invalid_command_that_does_not_exist")
    assert not result["success"]
    assert result["exit_code"] is not None and result["exit_code"] != 0


def test_execute_with_timeout(executor: CommandExecutor) -> None:
    """测试命令超时"""
    if platform.system().lower() == "windows":
        command = "timeout 2"
    else:
        command = "sleep 2"
    
    result = executor.execute(command, timeout=1)
    assert not result["success"]
    assert "超时" in result["stderr"]


def test_dangerous_command_detection(executor: CommandExecutor) -> None:
    """测试危险命令检测"""
    dangerous_commands = [
        "rm -rf /",
        "rm -rf /*",
        "dd if=/dev/zero of=/dev/sda",
        "> /etc/passwd",
        "chmod -R 777 /",
        "mkfs.ext4 /dev/sda",
    ]
    
    for cmd in dangerous_commands:
        is_dangerous, warnings = executor.is_dangerous(cmd)
        assert is_dangerous
        assert len(warnings) > 0


def test_working_directory(tmp_path: Path) -> None:
    """测试工作目录设置"""
    executor = CommandExecutor(working_dir=str(tmp_path))
    
    # 在Windows上使用不同的命令
    if platform.system().lower() == "windows":
        result = executor.execute("cd")
    else:
        result = executor.execute("pwd")
    
    assert result["success"]
    assert str(tmp_path) in result["stdout"].strip()


def test_environment_variables(executor: CommandExecutor) -> None:
    """测试环境变量设置"""
    env = {"TEST_VAR": "test_value"}
    
    # 在Windows上使用不同的命令
    if platform.system().lower() == "windows":
        result = executor.execute("echo %TEST_VAR%", env=env)
    else:
        result = executor.execute("echo $TEST_VAR", env=env)
    
    assert result["success"]
    assert "test_value" in result["stdout"]


def test_command_history(executor: CommandExecutor) -> None:
    """测试命令历史记录"""
    # 执行一系列命令
    commands = [
        "echo 'test1'",
        "echo 'test2'",
        "echo 'test3'",
    ]
    
    results = []
    for cmd in commands:
        result = executor.execute(cmd)
        results.append(result)
    
    # 验证所有命令都执行成功
    for result in results:
        assert result["success"]
        assert result["exit_code"] == 0


def test_shell_specific_features(executor: CommandExecutor) -> None:
    """测试特定shell的功能"""
    if executor.shell == "powershell":
        result = executor.execute("Get-Location")
    elif executor.shell == "cmd":
        result = executor.execute("cd")
    else:
        result = executor.execute("pwd")
    
    assert result["success"]
    assert result["exit_code"] == 0


def test_command_output_encoding(executor: CommandExecutor) -> None:
    """测试命令输出编码"""
    # 测试包含中文字符的命令
    if platform.system().lower() == "windows":
        result = executor.execute("echo 你好")
    else:
        result = executor.execute("echo '你好'")
    
    assert result["success"]
    assert "你好" in result["stdout"]


def test_error_handling(executor: CommandExecutor) -> None:
    """测试错误处理"""
    # 测试语法错误
    if platform.system().lower() == "windows":
        result = executor.execute("if (")
    else:
        result = executor.execute("if (;")
    
    assert not result["success"]
    assert result["stderr"] != ""
    assert result["exit_code"] != 0


@pytest.mark.parametrize("shell", ["bash", "zsh", "fish", "powershell", "cmd"])
def test_shell_selection(shell: str) -> None:
    """测试shell选择"""
    try:
        executor = CommandExecutor(shell=shell)
        # 只验证shell设置，不验证命令执行
        # 因为某些shell可能在测试环境中不可用
        assert executor.shell == shell
    except ValueError:
        # 如果shell不可用，跳过测试
        pytest.skip(f"Shell {shell} not available")


def test_command_validation(executor: CommandExecutor) -> None:
    """测试命令验证"""
    # 测试空命令
    with pytest.raises(ValueError):
        executor.execute("")
    
    # 测试None命令
    with pytest.raises(ValueError):
        executor.execute(None)  # type: ignore
    
    # 测试非字符串命令
    with pytest.raises(ValueError):
        executor.execute(123)  # type: ignore

