"""
pytest配置文件
"""

import os
import pytest
from pathlib import Path
from typing import Dict, Any, Generator

from ata.config_manager import ConfigManager
from ata.command_executor import CommandExecutor
from ata.cli import CLI
from ata.ai_interface import AIInterface


@pytest.fixture(scope="session")
def temp_config_dir(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """创建临时配置目录"""
    config_dir = tmp_path_factory.mktemp(".ata")
    return config_dir


@pytest.fixture(scope="session")
def config_manager(temp_config_dir: Path) -> ConfigManager:
    """创建配置管理器实例"""
    config_path = temp_config_dir / "config.yaml"
    return ConfigManager(str(config_path))


@pytest.fixture(scope="session")
def command_executor() -> CommandExecutor:
    """创建命令执行器实例"""
    return CommandExecutor()


@pytest.fixture(scope="session")
def ai_interface(config_manager: ConfigManager) -> AIInterface:
    """创建AI接口实例"""
    return AIInterface(config_manager)


@pytest.fixture(scope="session")
def cli(config_manager: ConfigManager, command_executor: CommandExecutor) -> CLI:
    """创建CLI实例"""
    return CLI(config_manager, command_executor)


@pytest.fixture(autouse=True)
def setup_test_env(monkeypatch: pytest.MonkeyPatch) -> Generator[None, None, None]:
    """设置测试环境"""
    # 设置测试环境变量
    monkeypatch.setenv("OPENAI_API_KEY", "test_openai_key")
    monkeypatch.setenv("DEEPSEEK_API_KEY", "test_deepseek_key")
    
    # 设置测试目录
    test_dir = Path(__file__).parent
    monkeypatch.chdir(test_dir)
    
    yield
    
    # 清理测试环境（如果需要）


@pytest.fixture
def mock_system_info() -> Dict[str, str]:
    """模拟系统信息"""
    return {
        "os": "Linux",
        "shell": "bash",
        "version": "5.4.0",
        "working_directory": "/home/user",
        "python_version": "3.8.10",
        "system_version": "Ubuntu 20.04",
        "machine": "x86_64"
    }


@pytest.fixture
def mock_config() -> Dict[str, Any]:
    """模拟配置"""
    return {
        "version": "1.0.0",
        "general": {
            "history_size": 20,
            "debug_mode": False,
            "working_directory": None
        },
        "ai": {
            "provider": "openai",
            "model": "gpt-4",
            "temperature": 0.7,
            "max_tokens": 2000
        },
        "security": {
            "dangerous_commands": [
                "rm -rf /",
                "rm -rf /*",
                "dd if=/dev/zero of=/dev/sda",
                "> /etc/passwd",
                "chmod -R 777 /",
                "mkfs.ext4 /dev/sda"
            ],
            "sensitive_directories": [
                "/etc",
                "/var",
                "/usr",
                "/boot",
                "/root"
            ],
            "require_confirmation": True
        },
        "ui": {
            "theme": "default",
            "colors": {
                "success": "green",
                "error": "red",
                "warning": "yellow",
                "info": "blue"
            },
            "show_welcome": True
        },
        "logging": {
            "level": "INFO",
            "file": None,
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    }


@pytest.fixture
def mock_command_result() -> Dict[str, Any]:
    """模拟命令执行结果"""
    return {
        "success": True,
        "command": "echo 'test'",
        "stdout": "test\n",
        "stderr": "",
        "exit_code": 0,
        "duration": 0.1,
        "warnings": []
    }


@pytest.fixture
def mock_ai_response() -> Dict[str, Any]:
    """模拟AI响应"""
    return {
        "choices": [{
            "message": {
                "content": """这是一个测试命令：

command: echo 'test'

explanation: 这是一个简单的测试命令，用于输出文本。

warnings: []"""
            }
        }]
    }


@pytest.fixture
def mock_history() -> Dict[str, Any]:
    """模拟历史记录"""
    return {
        "commands": [
            "echo 'test1'",
            "echo 'test2'",
            "echo 'test3'"
        ],
        "results": [
            {
                "success": True,
                "stdout": "test1\n",
                "stderr": "",
                "exit_code": 0
            },
            {
                "success": True,
                "stdout": "test2\n",
                "stderr": "",
                "exit_code": 0
            },
            {
                "success": True,
                "stdout": "test3\n",
                "stderr": "",
                "exit_code": 0
            }
        ]
    }


def pytest_configure(config: pytest.Config) -> None:
    """配置pytest"""
    # 添加自定义标记
    config.addinivalue_line(
        "markers",
        "integration: 标记集成测试"
    )
    config.addinivalue_line(
        "markers",
        "slow: 标记耗时测试"
    )
    config.addinivalue_line(
        "markers",
        "dangerous: 标记危险测试"
    )


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """修改测试项"""
    for item in items:
        # 为所有测试添加标记
        if "unit" not in item.keywords:
            item.add_marker(pytest.mark.unit)
        
        # 为集成测试添加标记
        if "integration" in item.keywords:
            item.add_marker(pytest.mark.integration)
        
        # 为耗时测试添加标记
        if "slow" in item.keywords:
            item.add_marker(pytest.mark.slow)
        
        # 为危险测试添加标记
        if "dangerous" in item.keywords:
            item.add_marker(pytest.mark.dangerous) 