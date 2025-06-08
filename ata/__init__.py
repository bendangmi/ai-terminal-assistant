"""
AI Terminal Assistant
"""

__version__ = "1.0.0"

from .ai_interface import AIInterface, Message
from .command_executor import CommandExecutor, CommandExecutionError, CommandResult
from .config_manager import ConfigManager
from .cli import CLI

__all__ = [
    "AIInterface",
    "Message",
    "CommandExecutor",
    "CommandExecutionError",
    "CommandResult",
    "ConfigManager",
    "CLI",
]

from typing import Dict, Any, Optional

__author__ = "AI Terminal Assistant Team"
__email__ = "corbing1031@gmail.com"
__license__ = "MIT"

def create_assistant(
    config_path: Optional[str] = None,
    provider: Optional[str] = None,
    model: Optional[str] = None,
    shell: Optional[str] = None,
    working_dir: Optional[str] = None
) -> CLI:
    """
    创建一个新的终端助手实例
    
    参数:
        config_path: 配置文件路径
        provider: AI提供商
        model: 模型名称
        shell: shell类型
        working_dir: 工作目录
        
    返回:
        CLI实例
    """
    # 创建配置管理器
    config_manager = ConfigManager(config_path)
    
    # 如果提供了参数，更新配置
    if provider:
        config_manager.set("ai.provider", provider)
    if model:
        config_manager.set(f"ai.providers.{provider or config_manager.get('ai.provider')}.model", model)
    if shell:
        config_manager.set("general.default_shell", shell)
    if working_dir:
        config_manager.set("general.working_directory", working_dir)
    
    # 创建AI接口
    current_provider = config_manager.get("ai.provider")
    provider_config = config_manager.get_provider_config(current_provider)
    ai_interface = AIInterface(
        provider=current_provider,
        model=provider_config.get("model"),
        fallback_provider=config_manager.get("ai.fallback_provider"),
        fallback_model=config_manager.get_provider_config(
            config_manager.get("ai.fallback_provider")
        ).get("model")
    )
    
    # 创建命令执行器
    command_executor = CommandExecutor(config_manager)
    
    # 创建CLI实例
    return CLI(
        ai_interface=ai_interface,
        command_executor=command_executor,
        config_manager=config_manager
    )

def execute_command(
    command: str,
    shell: Optional[str] = None,
    working_dir: Optional[str] = None,
    timeout: int = 30,
    env: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    执行单个命令
    
    参数:
        command: 要执行的命令
        shell: shell类型
        working_dir: 工作目录
        timeout: 超时时间（秒）
        env: 额外的环境变量
        
    返回:
        命令执行结果
    """
    config = ConfigManager()
    if shell:
        config.set("general.default_shell", shell)
    if working_dir:
        config.set("general.working_directory", working_dir)
        
    executor = CommandExecutor(config)
    return executor.execute(command, timeout=timeout, env=env)

def generate_command(
    user_input: str,
    provider: str = "openai",
    model: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    生成命令
    
    参数:
        user_input: 用户的自然语言请求
        provider: AI提供商
        model: 模型名称
        api_key: API密钥
        
    返回:
        生成的命令数据
    """
    ai_interface = AIInterface(
        provider=provider,
        model=model,
        api_key=api_key
    )
    
    config = ConfigManager()
    executor = CommandExecutor(config)
    system_info = executor.get_system_info()
    
    return ai_interface.generate_command(user_input, system_info) 