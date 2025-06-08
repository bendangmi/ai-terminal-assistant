import psutil
import os
import subprocess
import time
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
import platform

router = APIRouter()

class SystemInfo(BaseModel):
    cpu: Dict[str, Any]
    memory: Dict[str, Any]
    disk: Dict[str, Any]

class CommandRequest(BaseModel):
    command: str

class CommandOutput(BaseModel):
    type: str
    content: str
    timestamp: float

class CommandResponse(BaseModel):
    error: str = None
    output: List[CommandOutput] = []

@router.get("/", response_model=SystemInfo)
async def get_system_info():
    # CPU信息
    cpu_info = {
        "usage": psutil.cpu_percent(interval=1),
        "cores": psutil.cpu_count(),
        "frequency": psutil.cpu_freq().current / 1000 if psutil.cpu_freq() else 0
    }

    # 内存信息
    memory = psutil.virtual_memory()
    memory_info = {
        "total": memory.total,
        "available": memory.available,
        "percent": memory.percent,
        "used": memory.used,
        "free": memory.free
    }

    # 磁盘信息
    disk = psutil.disk_usage('/')
    disk_info = {
        "total": disk.total,
        "used": disk.used,
        "free": disk.free,
        "percent": disk.percent
    }

    return SystemInfo(
        cpu=cpu_info,
        memory=memory_info,
        disk=disk_info
    )

@router.get("/cpu")
async def get_cpu_info():
    return {
        "usage": psutil.cpu_percent(interval=1),
        "cores": psutil.cpu_count(),
        "frequency": psutil.cpu_freq().current / 1000 if psutil.cpu_freq() else 0
    }

@router.get("/memory")
async def get_memory_info():
    memory = psutil.virtual_memory()
    return {
        "total": memory.total,
        "available": memory.available,
        "percent": memory.percent,
        "used": memory.used,
        "free": memory.free
    }

@router.get("/disk")
async def get_disk_info():
    disk = psutil.disk_usage('/')
    return {
        "total": disk.total,
        "used": disk.used,
        "free": disk.free,
        "percent": disk.percent
    }

@router.get("/directory-info")
async def get_directory_info(path: str = "./") -> Dict:
    try:
        items = os.listdir(path)
        files = []
        directories = []
        
        for item in items:
            full_path = os.path.join(path, item)
            if os.path.isfile(full_path):
                files.append({
                    "name": item,
                    "size": os.path.getsize(full_path),
                    "modified": os.path.getmtime(full_path)
                })
            elif os.path.isdir(full_path):
                directories.append({
                    "name": item,
                    "modified": os.path.getmtime(full_path)
                })
        
        return {
            "current_path": os.path.abspath(path),
            "files": files,
            "directories": directories
        }
    except Exception as e:
        return {"error": str(e)}

@router.post("/execute", response_model=CommandResponse)
async def execute_command(command_req: CommandRequest):
    try:
        # 根据操作系统选择shell
        shell = True if platform.system() == "Windows" else False
        
        # 执行命令
        process = subprocess.Popen(
            command_req.command,
            shell=shell,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = process.communicate()
        
        response = CommandResponse()
        current_time = time.time()
        
        # 添加标准输出
        if stdout:
            response.output.append(
                CommandOutput(
                    type="output",
                    content=stdout.strip(),
                    timestamp=current_time
                )
            )
        
        # 添加错误输出
        if stderr:
            response.output.append(
                CommandOutput(
                    type="error",
                    content=stderr.strip(),
                    timestamp=current_time
                )
            )
        
        # 如果没有输出但命令执行失败
        if process.returncode != 0 and not (stdout or stderr):
            response.error = f"命令执行失败，返回码: {process.returncode}"
        
        return response
        
    except Exception as e:
        return CommandResponse(error=str(e)) 