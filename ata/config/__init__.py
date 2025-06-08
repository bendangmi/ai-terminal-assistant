import os
import yaml
import logging
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

class Config:
    """配置管理类"""
    
    def __init__(self, config_path: Optional[str] = None):
        """初始化配置管理器
        
        Args:
            config_path: 配置文件路径，如果为None则使用默认路径
        """
        self.config_path = config_path or self._get_default_config_path()
        self.config = self._load_config()
        
    def _get_default_config_path(self) -> str:
        """获取默认配置文件路径"""
        return os.path.join(os.path.dirname(__file__), "config.yaml")
        
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            if not os.path.exists(self.config_path):
                logger.warning(f"配置文件不存在: {self.config_path}，将使用默认配置")
                return self._get_default_config()
                
            with open(self.config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
                logger.info(f"成功加载配置文件: {self.config_path}")
                return config or self._get_default_config()
                
        except Exception as e:
            logger.error(f"加载配置文件失败: {str(e)}", exc_info=True)
            return self._get_default_config()
            
    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            "general": {
                "working_directory": None,
                "history_size": 1000,
                "log_level": "INFO"
            },
            "security": {
                "dangerous_commands": [
                    "rm -rf",
                    "deltree",
                    "format",
                    "mkfs",
                    "dd"
                ],
                "sensitive_directories": [
                    "/etc",
                    "/var",
                    "/usr",
                    "C:\\Windows",
                    "C:\\Program Files"
                ],
                "require_confirmation": True
            },
            "ai": {
                "provider": "openai",
                "model": "gpt-3.5-turbo",
                "temperature": 0.7,
                "max_tokens": 2000
            },
            "providers": {
                "openai": {
                    "api_key": "",
                    "organization": ""
                },
                "azure": {
                    "api_key": "",
                    "endpoint": "",
                    "deployment_name": ""
                }
            }
        }
        
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值
        
        Args:
            key: 配置键，使用点号分隔，如 "general.working_directory"
            default: 默认值
            
        Returns:
            配置值
        """
        try:
            value = self.config
            for k in key.split("."):
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
            
    def set(self, key: str, value: Any) -> None:
        """设置配置值
        
        Args:
            key: 配置键，使用点号分隔，如 "general.working_directory"
            value: 配置值
        """
        try:
            keys = key.split(".")
            current = self.config
            for k in keys[:-1]:
                if k not in current:
                    current[k] = {}
                current = current[k]
            current[keys[-1]] = value
            self._save_config()
            logger.info(f"成功设置配置: {key} = {value}")
        except Exception as e:
            logger.error(f"设置配置失败: {str(e)}", exc_info=True)
            
    def _save_config(self) -> None:
        """保存配置到文件"""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, "w", encoding="utf-8") as f:
                yaml.safe_dump(self.config, f, allow_unicode=True, default_flow_style=False)
            logger.info(f"成功保存配置文件: {self.config_path}")
        except Exception as e:
            logger.error(f"保存配置文件失败: {str(e)}", exc_info=True)
            
    def reload(self) -> None:
        """重新加载配置文件"""
        self.config = self._load_config()
        logger.info("成功重新加载配置文件") 