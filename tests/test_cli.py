"""
CLI界面测试模块
"""

import os
import pytest
from pathlib import Path
from typing import Dict, Any, List
from unittest.mock import MagicMock, patch

from ata.cli import CLI, CommandHistory
from ata.config_manager import ConfigManager
from ata.command_executor import CommandExecutor


@pytest.fixture
def temp_config_dir(tmp_path: Path) -> Path:
    """创建临时配置目录"""
    config_dir = tmp_path / ".ata"
    config_dir.mkdir()
    return config_dir


@pytest.fixture
def config_manager(temp_config_dir: Path) -> ConfigManager:
    """创建配置管理器实例"""
    config_path = temp_config_dir / "config.yaml"
    return ConfigManager(str(config_path))


@pytest.fixture
def command_executor() -> CommandExecutor:
    """创建命令执行器实例"""
    return CommandExecutor()


@pytest.fixture
def cli(config_manager: ConfigManager, command_executor: CommandExecutor) -> CLI:
    """创建CLI实例"""
    return CLI(config_manager, command_executor)


def test_cli_initialization(cli: CLI) -> None:
    """测试CLI初始化"""
    assert cli.config is not None
    assert cli.executor is not None
    assert cli.history is not None
    assert cli.debug_mode is False


def test_command_history(cli: CLI) -> None:
    """测试命令历史"""
    # 添加命令到历史记录
    cli.history.add("echo 'test1'")
    cli.history.add("echo 'test2'")
    cli.history.add("echo 'test3'")
    
    # 验证历史记录
    assert len(cli.history.commands) == 3
    assert cli.history.commands[-1] == "echo 'test3'"
    
    # 测试历史记录导航
    assert cli.history.get_previous() == "echo 'test3'"
    assert cli.history.get_previous() == "echo 'test2'"
    assert cli.history.get_previous() == "echo 'test1'"
    assert cli.history.get_previous() == "echo 'test1'"  # 到达开头
    
    assert cli.history.get_next() == "echo 'test2'"
    assert cli.history.get_next() == "echo 'test3'"
    assert cli.history.get_next() == "echo 'test3'"  # 到达末尾


def test_command_execution(cli: CLI) -> None:
    """测试命令执行"""
    # 执行简单命令
    result = cli.execute_command("echo 'test'")
    assert result["success"]
    assert "test" in result["stdout"]
    
    # 执行无效命令
    result = cli.execute_command("invalid_command")
    assert not result["success"]
    assert result["stderr"] != ""


def test_command_confirmation(cli: CLI) -> None:
    """测试命令确认"""
    # 模拟用户输入
    with patch("builtins.input", return_value="y"):
        assert cli.confirm_command("rm -rf test_dir")
    
    with patch("builtins.input", return_value="n"):
        assert not cli.confirm_command("rm -rf test_dir")


def test_command_editing(cli: CLI) -> None:
    """测试命令编辑"""
    # 模拟用户输入
    with patch("builtins.input", return_value="echo 'modified'"):
        command = cli.edit_command("echo 'original'")
        assert command == "echo 'modified'"


def test_debug_mode(cli: CLI) -> None:
    """测试调试模式"""
    # 启用调试模式
    cli.set_debug_mode(True)
    assert cli.debug_mode is True
    
    # 执行命令并验证详细输出
    result = cli.execute_command("echo 'test'")
    assert result["success"]
    assert "duration" in result
    assert "exit_code" in result


def test_command_validation(cli: CLI) -> None:
    """测试命令验证"""
    # 测试空命令
    with pytest.raises(ValueError):
        cli.execute_command("")
    
    # 测试危险命令
    result = cli.execute_command("rm -rf /", skip_confirmation=False)
    assert not result["success"]
    assert "危险命令" in result["stderr"]


def test_error_handling(cli: CLI) -> None:
    """测试错误处理"""
    # 测试超时
    result = cli.execute_command("sleep 10", timeout=1)
    assert not result["success"]
    assert "超时" in result["stderr"]
    
    # 测试中断
    with patch("ata.command_executor.subprocess.Popen") as mock_popen:
        mock_process = MagicMock()
        mock_process.communicate.side_effect = KeyboardInterrupt()
        mock_popen.return_value = mock_process
        
        result = cli.execute_command("long_running_command")
        assert not result["success"]
        assert "中断" in result["stderr"]


def test_welcome_screen(cli: CLI) -> None:
    """测试欢迎界面"""
    welcome_text = cli.get_welcome_text()
    assert "欢迎" in welcome_text
    assert "版本" in welcome_text
    assert "帮助" in welcome_text


def test_command_suggestions(cli: CLI) -> None:
    """测试命令建议"""
    # 添加一些历史命令
    cli.history.add("git status")
    cli.history.add("git commit -m 'test'")
    cli.history.add("git push")
    
    # 获取建议
    suggestions = cli.get_command_suggestions("git")
    assert len(suggestions) > 0
    assert all(cmd.startswith("git") for cmd in suggestions)


def test_command_completion(cli: CLI) -> None:
    """测试命令补全"""
    # 添加一些历史命令
    cli.history.add("echo 'test1'")
    cli.history.add("echo 'test2'")
    cli.history.add("git status")
    
    # 测试命令补全
    completions = cli.get_command_completions("ec")
    assert "echo" in completions
    
    completions = cli.get_command_completions("git")
    assert "git status" in completions


def test_output_formatting(cli: CLI) -> None:
    """测试输出格式化"""
    # 测试成功输出
    success_output = cli.format_output({
        "success": True,
        "stdout": "test output",
        "stderr": "",
        "exit_code": 0
    })
    assert "test output" in success_output
    assert "成功" in success_output
    
    # 测试错误输出
    error_output = cli.format_output({
        "success": False,
        "stdout": "",
        "stderr": "error message",
        "exit_code": 1
    })
    assert "error message" in error_output
    assert "错误" in error_output


def test_help_system(cli: CLI) -> None:
    """测试帮助系统"""
    help_text = cli.get_help_text()
    assert "使用方法" in help_text
    assert "命令" in help_text
    assert "选项" in help_text
    
    # 测试特定命令的帮助
    command_help = cli.get_command_help("history")
    assert "历史记录" in command_help


def test_logging_system(cli: CLI, temp_config_dir: Path) -> None:
    """测试日志系统"""
    # 设置日志文件
    log_file = temp_config_dir / "ata.log"
    cli.setup_logging(str(log_file))
    
    # 执行一些命令
    cli.execute_command("echo 'test'")
    cli.execute_command("invalid_command")
    
    # 验证日志文件
    assert log_file.exists()
    log_content = log_file.read_text()
    assert "echo 'test'" in log_content
    assert "invalid_command" in log_content


def test_interactive_mode(cli: CLI) -> None:
    """测试交互模式"""
    # 模拟用户输入
    with patch("builtins.input", side_effect=["echo 'test'", "exit"]):
        # 运行交互模式
        with pytest.raises(SystemExit):
            cli.run_interactive()


def test_command_history_persistence(cli: CLI, temp_config_dir: Path) -> None:
    """测试命令历史持久化"""
    history_file = temp_config_dir / "history.txt"
    
    # 添加一些命令
    cli.history.add("command1")
    cli.history.add("command2")
    cli.history.add("command3")
    
    # 保存历史记录
    cli.history.save(str(history_file))
    
    # 创建新的历史记录并加载
    new_history = CommandHistory()
    new_history.load(str(history_file))
    
    # 验证历史记录
    assert len(new_history.commands) == 3
    assert new_history.commands == ["command1", "command2", "command3"]


def test_environment_handling(cli: CLI) -> None:
    """测试环境变量处理"""
    # 设置环境变量
    test_env = {"TEST_VAR": "test_value"}
    
    # 执行使用环境变量的命令
    if os.name == "nt":  # Windows
        result = cli.execute_command("echo %TEST_VAR%", env=test_env)
    else:  # Unix-like
        result = cli.execute_command("echo $TEST_VAR", env=test_env)
    
    assert result["success"]
    assert "test_value" in result["stdout"]


def test_signal_handling(cli: CLI) -> None:
    """测试信号处理"""
    # 模拟SIGINT信号
    with patch("signal.signal") as mock_signal:
        cli.setup_signal_handlers()
        mock_signal.assert_called()


def test_unicode_handling(cli: CLI) -> None:
    """测试Unicode处理"""
    # 测试包含Unicode字符的命令
    result = cli.execute_command("echo '你好，世界！'")
    assert result["success"]
    assert "你好，世界！" in result["stdout"]


def test_performance_monitoring(cli: CLI) -> None:
    """测试性能监控"""
    # 执行命令并检查性能指标
    with cli.monitor_performance():
        result = cli.execute_command("echo 'test'")
    
    assert result["success"]
    assert "duration" in result
    assert isinstance(result["duration"], float)
    assert result["duration"] >= 0 