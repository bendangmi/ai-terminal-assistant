from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests
from typing import Dict, Optional
import json
import os

router = APIRouter()

class ServerConfig(BaseModel):
    host: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None
    protocol: str = "http"

class LLMConfig(BaseModel):
    api_key: str
    model_name: str
    api_base: Optional[str] = None
    organization: Optional[str] = None

@router.post("/test-server-connection")
async def test_server_connection(config: ServerConfig) -> Dict:
    try:
        url = f"{config.protocol}://{config.host}:{config.port}"
        auth = None
        if config.username and config.password:
            auth = (config.username, config.password)
        
        response = requests.get(url, auth=auth, timeout=5)
        return {
            "status": "success",
            "message": f"成功连接到服务器 {url}",
            "response_code": response.status_code
        }
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=400, detail="无法连接到服务器")
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=408, detail="连接超时")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/test-llm-config")
async def test_llm_config(config: LLMConfig) -> Dict:
    try:
        # 保存配置到文件
        config_path = "config.json"
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                current_config = json.load(f)
        else:
            current_config = {}
        
        current_config["llm"] = config.dict()
        
        with open(config_path, "w") as f:
            json.dump(current_config, f, indent=4)
        
        # 测试API连接
        headers = {
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json"
        }
        
        if config.organization:
            headers["OpenAI-Organization"] = config.organization
            
        api_base = config.api_base or "https://api.openai.com/v1"
        url = f"{api_base}/models"
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        return {
            "status": "success",
            "message": "大模型配置测试成功",
            "available_models": response.json()
        }
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"API请求失败: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 