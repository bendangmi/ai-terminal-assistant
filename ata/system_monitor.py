"""
系统监控模块
"""

import psutil
import os
import platform
from typing import Dict, Any
from pathlib import Path

class SystemMonitor:
    """系统监控类"""
    
    @staticmethod
    def get_system_info() -> Dict[str, Any]:
        """获取系统信息
        
        Returns:
            包含系统信息的字典
        """
        # CPU信息
        cpu_info = {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "cpu_count": psutil.cpu_count(),
            "cpu_freq": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None
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
        
        # 操作系统信息
        os_info = {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor()
        }
        
        # 当前工作目录信息
        current_dir = os.getcwd()
        dir_contents = []
        try:
            for item in Path(current_dir).iterdir():
                dir_contents.append({
                    "name": item.name,
                    "type": "directory" if item.is_dir() else "file",
                    "size": os.path.getsize(item) if item.is_file() else None,
                    "modified": os.path.getmtime(item)
                })
        except Exception as e:
            dir_contents = [{"error": str(e)}]
            
        return {
            "cpu": cpu_info,
            "memory": memory_info,
            "disk": disk_info,
            "os": os_info,
            "current_dir": {
                "path": current_dir,
                "contents": dir_contents
            }
        } 