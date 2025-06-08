"""
配置管理模块

负责加载和保存用户配置。
提供配置验证和迁移功能。
"""

import os
import yaml
import json
import shutil
from typing import Dict, Any, Optional, List, Union
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime
import logging

from .exceptions import ConfigError

logger = logging.getLogger(__name__)


@dataclass
class ConfigValidationError:
    """配置验证错误"""
    path: str
    message: str
    value: Any


class ConfigManager:
    """配置管理类，负责加载和保存用户配置"""

    # 配置模式定义
    CONFIG_SCHEMA = {
        "version": "1.0.0",  # 配置文件版本
        "general": {
            "web_server": {
                "host": "127.0.0.1",
                "port": 8000,
                "debug": False
            },
            "history_size": 20,
            "debug_mode": False,
            "working_directory": None
        },
        "ai": {
            "provider": "deepseek",  # 默认使用 deepseek
            "max_history_length": 100,
            "max_context_length": 4000,
            "deepseek": {
                "model": "deepseek-coder",
                "temperature": 0.7,
                "max_tokens": 2000,
                "api_key": None,  # 直接存储API密钥
                "api_key_env": "DEEPSEEK_API_KEY",  # 环境变量名
                "models": [
                    "deepseek-chat",
                    "deepseek-coder"
                ]
            },
            "openai": {
                "model": "gpt-4",
                "temperature": 0.7,
                "max_tokens": 2000,
                "api_key": None,  # 直接存储API密钥
                "api_key_env": "OPENAI_API_KEY",  # 环境变量名
                "models": [
                    "gpt-4",
                    "gpt-4-turbo",
                    "gpt-3.5-turbo"
                ]
            }
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

    def __init__(self, config_file: Optional[Union[str, Path]] = None):
        """初始化配置管理器
        
        Args:
            config_file: 配置文件路径，如果为None则使用默认路径
        """
        if config_file is None:
            # 使用项目根目录下的config.yaml
            self.config_file = Path(__file__).parent.parent / 'config.yaml'
        else:
            self.config_file = Path(config_file)
        
        self.config: Dict[str, Any] = {}
        self.load()
    
    def load(self):
        """加载配置文件"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = yaml.safe_load(f) or {}
                logger.info(f"已加载配置文件: {self.config_file}")
            else:
                logger.warning(f"配置文件不存在: {self.config_file}")
                # 使用默认配置
                self.config = self.CONFIG_SCHEMA.copy()
                self.save()
        except Exception as e:
            logger.error(f"加载配置文件失败: {str(e)}")
            raise ConfigError(f"加载配置文件失败: {str(e)}")
    
    def save(self):
        """保存配置到文件"""
        try:
            # 确保配置文件目录存在
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                yaml.safe_dump(self.config, f, allow_unicode=True, sort_keys=False)
            logger.info(f"已保存配置文件: {self.config_file}")
        except Exception as e:
            logger.error(f"保存配置文件失败: {str(e)}")
            raise ConfigError(f"保存配置文件失败: {str(e)}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值
        
        Args:
            key: 配置键，使用点号分隔层级
            default: 默认值
            
        Returns:
            配置值
        """
        try:
            value = self.config
            for k in key.split('.'):
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any):
        """设置配置值
        
        Args:
            key: 配置键，使用点号分隔层级
            value: 配置值
        """
        keys = key.split('.')
        current = self.config
        
        # 遍历到最后一个键之前
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        
        # 设置最后一个键的值
        current[keys[-1]] = value
    
    def _get_default_config_dir(self) -> str:
        """获取默认配置目录路径"""
        if os.name == "nt":  # Windows
            base_dir = os.environ.get("APPDATA", os.path.expanduser("~"))
            return os.path.join(base_dir, "ata")
        else:  # Unix-like
            base_dir = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
            return os.path.join(base_dir, "ata")
    
    def _create_backup(self) -> None:
        """创建配置文件的备份"""
        if not self.config_file.exists():
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.config_file.parent / f"config_{timestamp}.json"
        
        # 复制配置文件
        shutil.copy2(self.config_file, backup_path)
        
        # 清理旧备份（保留最近10个）
        backups = sorted(self.config_file.parent.glob("config_*.json"))
        if len(backups) > 10:
            for old_backup in backups[:-10]:
                old_backup.unlink()
    
    def _migrate_config(self, old_config: Dict[str, Any]) -> Dict[str, Any]:
        """迁移旧版本配置到新版本"""
        # 创建配置备份
        self._create_backup()
        
        # 获取旧配置版本
        old_version = old_config.get("version", "0.0.0")
        
        # 在这里添加迁移逻辑
        # 例如：if old_version == "0.9.0": ...
        
        # 设置新版本号
        old_config["version"] = self.CONFIG_SCHEMA["version"]
        
        return old_config
    
    def _merge_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """合并配置与默认值"""
        merged = {}
        
        def merge_dict(base: Dict[str, Any], update: Dict[str, Any]) -> None:
            for key, value in update.items():
                if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                    if not key in merged:
                        merged[key] = {}
                    merge_dict(base[key], value)
                else:
                    if key in base:
                        merged[key] = value
                    else:
                        merged[key] = base.get(key, value)
        
        # 首先复制默认配置
        merged = self.CONFIG_SCHEMA.copy()
        
        # 然后用用户配置覆盖默认值
        for key, value in config.items():
            if isinstance(value, dict) and key in merged and isinstance(merged[key], dict):
                merged[key].update(value)
            else:
                merged[key] = value
        
        return merged
    
    def validate_config(self) -> List[ConfigValidationError]:
        """验证整个配置
        
        Returns:
            错误列表
        """
        errors = []
        
        # 验证general部分
        if not isinstance(self.config.get("general", {}).get("history_size"), int):
            errors.append(ConfigValidationError("general.history_size", "必须是整数"))
        
        # 验证AI部分
        ai_config = self.config.get("ai", {})
        if "provider" not in ai_config:
            errors.append(ConfigValidationError("ai.provider", "必须指定提供商"))
        elif ai_config["provider"] not in ["openai", "deepseek"]:
            errors.append(ConfigValidationError("ai.provider", "不支持的提供商"))
        
        # 验证每个提供商的配置
        for provider in ["openai", "deepseek"]:
            provider_config = ai_config.get(provider, {})
            if "model" not in provider_config:
                errors.append(ConfigValidationError(f"ai.{provider}.model", "必须指定模型"))
            if "api_key_env" not in provider_config:
                errors.append(ConfigValidationError(f"ai.{provider}.api_key_env", "必须指定API密钥环境变量"))
        
        return errors
    
    def save_config(self) -> bool:
        """保存配置到文件
        
        Returns:
            是否保存成功
            
        Raises:
            ConfigError: 配置保存错误
        """
        try:
            # 创建备份
            self._create_backup()
            
            # 保存配置
            self.save()
            
            return True
        except Exception as e:
            logger.error(f"保存配置文件失败: {str(e)}")
            raise ConfigError(f"保存配置文件失败: {str(e)}")
    
    def get_provider_config(self, provider: Optional[str] = None) -> Dict[str, Any]:
        """获取指定提供商的配置
        
        Args:
            provider: 提供商名称，如果为None则使用当前配置的提供商
            
        Returns:
            提供商配置
            
        Raises:
            ValueError: 当提供商配置不存在时
        """
        if provider is None:
            provider = self.get("ai.provider", "deepseek")
        
        provider_config = self.get(f"ai.{provider}")
        if not provider_config:
            # 如果配置不存在，使用默认配置
            provider_config = self.CONFIG_SCHEMA["ai"].get(provider, {})
            if not provider_config:
                raise ValueError(f"不支持的AI提供商: {provider}")
            
            # 保存默认配置
            if "ai" not in self.config:
                self.config["ai"] = {}
            self.config["ai"][provider] = provider_config.copy()
            self.save()
        
        return provider_config
    
    def get_available_providers(self) -> List[str]:
        """获取所有可用的提供商
        
        Returns:
            提供商名称列表
        """
        providers = self.get("ai", {})
        return list(providers.keys())
    
    def get_model_for_provider(self, provider: str) -> str:
        """获取指定提供商的模型
        
        Args:
            provider: 提供商名称
            
        Returns:
            模型名称
        """
        provider_config = self.get_provider_config(provider)
        return provider_config.get("model", "")
    
    def get_api_key_env_for_provider(self, provider: str) -> str:
        """获取指定提供商的API密钥环境变量名
        
        Args:
            provider: 提供商名称
            
        Returns:
            API密钥环境变量名
        """
        provider_config = self.get_provider_config(provider)
        return provider_config.get("api_key_env", "")
    
    def reset_to_defaults(self) -> bool:
        """将配置重置为默认值
        
        Returns:
            是否重置成功
        """
        try:
            # 创建备份
            self._create_backup()
            
            # 加载默认配置
            self.config = self._load_config()
            
            # 保存配置
            return self.save_config()
        
        except Exception as e:
            print(f"重置配置时出错: {str(e)}")
            return False
    
    def export_config(self, export_path: Union[str, Path]) -> bool:
        """导出配置到文件
        
        Args:
            export_path: 导出文件路径
            
        Returns:
            是否导出成功
            
        Raises:
            ConfigError: 配置导出错误
        """
        try:
            export_path = Path(export_path)
            
            # 确保目录存在
            export_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 导出配置
            self.save()
            
            return True
        except Exception as e:
            logger.error(f"导出配置失败: {str(e)}")
            raise ConfigError(f"导出配置失败: {str(e)}")
    
    def import_config(self, import_path: Union[str, Path]) -> bool:
        """从文件导入配置
        
        Args:
            import_path: 导入文件路径
            
        Returns:
            是否导入成功
            
        Raises:
            ConfigError: 配置导入错误
        """
        try:
            import_path = Path(import_path)
            
            # 检查文件是否存在
            if not import_path.exists():
                raise ConfigError(f"导入文件不存在: {import_path}")
            
            # 读取配置
            self.config = json.loads(import_path.read_text())
            
            # 验证配置版本
            if self.config.get("version") != self.CONFIG_SCHEMA["version"]:
                logger.warning("导入配置版本不匹配，将进行迁移")
                self.config = self._migrate_config(self.config)
            
            # 合并配置
            self.config = self._merge_config(self.config)
            
            # 保存配置
            self.save()
            
            return True
        except Exception as e:
            logger.error(f"导入配置失败: {str(e)}")
            raise ConfigError(f"导入配置失败: {str(e)}")
    
    def get_api_key(self, provider: str) -> Optional[str]:
        """获取API密钥
        
        首先尝试从环境变量获取，如果未找到则从配置文件获取
        
        Args:
            provider: 提供商名称
            
        Returns:
            API密钥或None
        """
        # 获取环境变量名
        env_name = self.get(f"ai.{provider}.api_key_env")
        if not env_name:
            return None
        
        # 尝试从环境变量获取
        api_key = os.environ.get(env_name)
        if api_key:
            return api_key
        
        # 从配置文件获取
        return self.get(f"ai.{provider}.api_key")
    
    def set_api_key(self, provider: str, api_key: str) -> None:
        """设置API密钥
        
        Args:
            provider: 提供商名称
            api_key: API密钥
        """
        self.set(f"ai.{provider}.api_key", api_key)
        self.save()

