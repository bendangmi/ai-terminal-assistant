from fastapi import APIRouter
from pydantic import BaseModel
import psutil
import time
import platform

router = APIRouter()

class Status(BaseModel):
    status: str
    uptime: float
    cpu_usage: float
    memory_usage: float
    platform: str
    python_version: str

start_time = time.time()

@router.get("/", response_model=Status)
async def get_status():
    """获取系统状态"""
    return {
        "status": "running",
        "uptime": time.time() - start_time,
        "cpu_usage": psutil.cpu_percent(),
        "memory_usage": psutil.virtual_memory().percent,
        "platform": platform.platform(),
        "python_version": platform.python_version()
    } 