import subprocess
import platform
import time
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging
from ..command_executor import CommandExecutor
from ..config import Config

# 配置日志
logger = logging.getLogger(__name__)

router = APIRouter()

class CommandRequest(BaseModel):
    command: str
    working_directory: Optional[str] = None

class CommandOutput(BaseModel):
    type: str  # 'output' or 'error'
    content: str
    timestamp: float

class CommandResponse(BaseModel):
    error: Optional[str] = None
    output: List[CommandOutput] = []
    exit_code: Optional[int] = None

@router.post("/execute")
async def execute_command(request: CommandRequest) -> Dict[str, Any]:
    """
    执行命令API
    
    Args:
        request: 命令请求对象
        
    Returns:
        执行结果
    """
    try:
        logger.info(f"收到命令执行请求: {request.dict()}")
        
        # 获取配置
        config = Config()
        executor = CommandExecutor(config)
        
        # 执行命令
        result = executor.execute(
            command=request.command,
            working_directory=request.working_directory
        )
        
        # 格式化输出
        output = []
        if result["stdout"]:
            output.append({
                "type": "output",
                "content": result["stdout"],
                "timestamp": result["timestamp"]
            })
        if result["stderr"]:
            output.append({
                "type": "error",
                "content": result["stderr"],
                "timestamp": result["timestamp"]
            })
            
        logger.debug(f"命令执行结果: {result}")
        
        return {
            "success": result["success"],
            "output": output
        }
        
    except Exception as e:
        logger.error(f"命令执行失败: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"命令执行失败: {str(e)}"
        ) 