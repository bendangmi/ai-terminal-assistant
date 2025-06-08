import yaml
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import os
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class Settings(BaseModel):
    ai: Dict[str, Any]
    general: Dict[str, Any]
    logging: Dict[str, Any]
    ui: Dict[str, Any]

@router.get("/")
async def get_settings():
    """获取当前设置"""
    try:
        config_path = "config.yaml"
        logger.info(f"正在读取配置文件: {config_path}")
        
        if not os.path.exists(config_path):
            logger.warning(f"配置文件不存在: {config_path}")
            return {
                "ai": {
                    "provider": "deepseek",
                    "deepseek": {
                        "model": "deepseek-coder",
                        "temperature": 0.7,
                        "api_key": ""
                    }
                },
                "general": {
                    "history_size": 20,
                    "debug_mode": False,
                    "auto_start": False
                },
                "logging": {
                    "level": "INFO"
                },
                "ui": {
                    "terminal": {
                        "font_size": 14,
                        "font_family": "Consolas",
                        "theme": "dark",
                        "history_size": 100
                    }
                }
            }
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            logger.debug(f"已加载配置: {config}")
            return config
            
    except Exception as e:
        logger.error(f"获取设置失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
async def update_settings(settings: Settings):
    """更新设置"""
    try:
        config_path = "config.yaml"
        logger.info(f"正在更新配置文件: {config_path}")
        logger.debug(f"新配置: {settings.dict()}")
        
        # 如果文件存在，先读取现有配置
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                current_config = yaml.safe_load(f) or {}
        else:
            current_config = {}
        
        # 更新配置
        new_config = settings.dict()
        
        # 合并AI配置
        if "ai" in new_config:
            if "ai" not in current_config:
                current_config["ai"] = {}
            current_config["ai"].update(new_config["ai"])
            
            # 确保提供商配置存在
            provider = current_config["ai"].get("provider")
            if provider and provider not in current_config["ai"]:
                current_config["ai"][provider] = {}
        
        # 合并其他配置
        if "general" in new_config:
            current_config["general"] = new_config["general"]
        if "logging" in new_config:
            current_config["logging"] = new_config["logging"]
        if "ui" in new_config:
            current_config["ui"] = new_config["ui"]
        
        logger.debug(f"合并后的配置: {current_config}")
        
        # 保存配置
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(current_config, f, allow_unicode=True, sort_keys=False)
            
        logger.info("配置更新成功")
        return current_config
        
    except Exception as e:
        logger.error(f"更新设置失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e)) 