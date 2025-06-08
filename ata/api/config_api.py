from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from pathlib import Path
import yaml
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class ConfigUpdate(BaseModel):
    section: str
    config: Dict[str, Any]

@router.post("/save-config")
async def save_config(update: ConfigUpdate):
    """保存配置到文件"""
    try:
        config_path = Path("config.yaml")
        
        # 读取现有配置
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
        else:
            config = {}
        
        # 更新配置
        if update.section == 'server':
            if 'general' not in config:
                config['general'] = {}
            if 'web_server' not in config['general']:
                config['general']['web_server'] = {}
            config['general']['web_server'].update(update.config)
        
        elif update.section == 'ai':
            if 'ai' not in config:
                config['ai'] = {}
            # 更新AI提供商配置
            provider = update.config.pop('provider', None)
            if provider:
                config['ai']['provider'] = provider
                if provider not in config['ai']:
                    config['ai'][provider] = {}
                config['ai'][provider].update({
                    'model': update.config.get('model'),
                    'api_key': update.config.get('apiKey'),
                    'temperature': update.config.get('temperature', 0.7),
                    'max_tokens': update.config.get('maxTokens', 2000)
                })
        
        elif update.section == 'system':
            if 'general' not in config:
                config['general'] = {}
            config['general'].update({
                'debug_mode': update.config.get('debugMode', False),
                'history_size': update.config.get('historySize', 20)
            })
            if 'logging' not in config:
                config['logging'] = {}
            config['logging'].update({
                'level': update.config.get('logLevel', 'INFO')
            })
        
        # 保存配置
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(config, f, allow_unicode=True, sort_keys=False)
        
        return {"status": "success", "message": "配置已保存"}
    
    except Exception as e:
        logger.error(f"保存配置失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get-config")
async def get_config():
    """获取当前配置"""
    try:
        config_path = Path("config.yaml")
        if not config_path.exists():
            return {
                "server": {
                    "host": "127.0.0.1",
                    "port": 8000,
                    "protocol": "http"
                },
                "ai": {
                    "provider": "deepseek",
                    "model": "deepseek-coder",
                    "temperature": 0.7,
                    "maxTokens": 2000
                },
                "system": {
                    "debugMode": False,
                    "historySize": 20,
                    "logLevel": "INFO"
                }
            }
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # 转换配置格式以匹配前端需求
        return {
            "server": {
                "host": config.get('general', {}).get('web_server', {}).get('host', '127.0.0.1'),
                "port": config.get('general', {}).get('web_server', {}).get('port', 8000),
                "protocol": config.get('general', {}).get('web_server', {}).get('protocol', 'http')
            },
            "ai": {
                "provider": config.get('ai', {}).get('provider', 'deepseek'),
                "model": config.get('ai', {}).get(config.get('ai', {}).get('provider', 'deepseek'), {}).get('model', 'deepseek-coder'),
                "temperature": config.get('ai', {}).get(config.get('ai', {}).get('provider', 'deepseek'), {}).get('temperature', 0.7),
                "maxTokens": config.get('ai', {}).get(config.get('ai', {}).get('provider', 'deepseek'), {}).get('max_tokens', 2000)
            },
            "system": {
                "debugMode": config.get('general', {}).get('debug_mode', False),
                "historySize": config.get('general', {}).get('history_size', 20),
                "logLevel": config.get('logging', {}).get('level', 'INFO')
            }
        }
    
    except Exception as e:
        logger.error(f"获取配置失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 