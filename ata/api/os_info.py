import os
import psutil
from fastapi import APIRouter, HTTPException
from typing import Dict, List
import platform

router = APIRouter()

@router.get("/cpu")
async def get_cpu_info() -> Dict:
    """获取CPU信息"""
    try:
        return {
            "usage": psutil.cpu_percent(interval=1),
            "cores": psutil.cpu_count(),
            "frequency": psutil.cpu_freq().current / 1000 if psutil.cpu_freq() else 0,
            "architecture": platform.machine(),
            "processor": platform.processor()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/memory")
async def get_memory_info() -> Dict:
    """获取内存信息"""
    try:
        memory = psutil.virtual_memory()
        return {
            "total": memory.total,
            "available": memory.available,
            "percent": memory.percent,
            "used": memory.used,
            "free": memory.free
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/disk")
async def get_disk_info() -> Dict:
    """获取磁盘信息"""
    try:
        disk = psutil.disk_usage('/')
        return {
            "total": disk.total,
            "used": disk.used,
            "free": disk.free,
            "percent": disk.percent
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/current-directory")
async def get_current_directory():
    """获取当前目录"""
    try:
        return {
            "path": os.getcwd(),
            "separator": os.path.sep
        }
    except Exception as e:
        return {"error": str(e)}

@router.get("/directory-contents")
async def get_directory_contents(path: str = None):
    """获取目录内容"""
    try:
        target_path = path or os.getcwd()
        contents = []
        
        for item in os.listdir(target_path):
            item_path = os.path.join(target_path, item)
            try:
                stats = os.stat(item_path)
                contents.append({
                    "name": item,
                    "path": item_path,
                    "is_dir": os.path.isdir(item_path),
                    "size": stats.st_size,
                    "modified": stats.st_mtime,
                    "created": stats.st_ctime
                })
            except Exception:
                continue
                
        return {
            "path": target_path,
            "contents": contents
        }
    except Exception as e:
        return {"error": str(e)} 