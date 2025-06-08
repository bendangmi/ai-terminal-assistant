from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from ..ai_interface import AIInterface
from ..config_manager import ConfigManager
from ..command_executor import CommandExecutor
import logging
import os

logger = logging.getLogger(__name__)

router = APIRouter()

class AIExecuteRequest(BaseModel):
    command: str
    working_directory: Optional[str] = None

@router.post("/execute")
async def execute_ai_command(request: AIExecuteRequest) -> Dict[str, Any]:
    """执行AI命令
    
    Args:
        request: AI执行请求
        
    Returns:
        执行结果
        
    Raises:
        HTTPException: 当执行出错时
    """
    try:
        logger.info(f"收到AI执行请求: {request.command}")
        
        # 创建配置管理器
        config = ConfigManager()
        logger.debug("配置管理器创建成功")
        
        # 获取当前AI提供商配置
        provider = config.get("ai.provider", "deepseek")
        logger.info(f"当前AI提供商: {provider}")
        
        provider_config = config.get_provider_config(provider)
        if not provider_config:
            logger.error(f"无法获取提供商配置: {provider}")
            raise ValueError(f"无法获取提供商配置: {provider}")
            
        logger.debug(f"提供商配置: {provider_config}")
        
        # 获取模型和API密钥
        model = provider_config.get("model")
        api_key = provider_config.get("api_key")
        
        # 如果API密钥未在配置中设置，尝试从环境变量获取
        if not api_key:
            env_key = provider_config.get("api_key_env")
            if env_key:
                api_key = os.environ.get(env_key)
        
        if not model:
            logger.error(f"未配置模型: {provider}")
            raise ValueError(f"未配置模型: {provider}")
            
        if not api_key:
            logger.error(f"未配置API密钥: {provider}")
            raise ValueError(f"未配置API密钥: {provider}")
            
        logger.info(f"使用模型: {model}")
        
        # 创建AI接口
        ai_interface = AIInterface(
            provider=provider,
            model=model,
            api_key=api_key
        )
        logger.debug("AI接口创建成功")
        
        # 创建命令执行器
        executor = CommandExecutor(config)
        logger.debug("命令执行器创建成功")
        
        # 获取系统信息
        system_info = executor.get_system_info()
        logger.debug(f"系统信息: {system_info}")
        
        # 生成命令
        try:
            logger.info("开始生成命令...")
            command_data = await ai_interface.generate_command(
                user_input=request.command,
                system_info=system_info
            )
            logger.info(f"命令生成成功: {command_data}")
            
            if not isinstance(command_data, dict):
                logger.error(f"AI返回的命令格式无效: {command_data}")
                raise ValueError("AI返回的命令格式无效")
                
            command = command_data.get("command")
            explanation = command_data.get("explanation", "")
            warnings = command_data.get("warnings", [])
            
            if not command:
                logger.error("AI未返回有效命令")
                raise ValueError("AI未返回有效命令")
            
            logger.info(f"命令解析成功 - 命令: {command}, 解释: {explanation}, 警告: {warnings}")
            
            return {
                "success": True,
                "command": command,
                "explanation": explanation,
                "warnings": warnings
            }
            
        except Exception as e:
            logger.error(f"AI命令生成失败: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=400,
                detail=f"AI无法理解您的输入: {str(e)}"
            )
            
    except Exception as e:
        logger.error(f"AI执行失败: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"AI执行出错: {str(e)}"
        ) 