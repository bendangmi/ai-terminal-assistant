"""
AI Terminal Assistant 主入口模块
"""

import os
import logging
import logging.config
import yaml
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import execute, ai, settings, os_info

from .config_manager import ConfigManager
from .web_server import WebServer

# 配置日志
def setup_logging():
    """配置日志系统"""
    log_config_path = Path(__file__).parent / "config" / "logging.yaml"
    if log_config_path.exists():
        with open(log_config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

# 创建应用
app = FastAPI(
    title="AI Terminal Assistant",
    description="一个基于Python和Vue的AI终端助手系统",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(execute.router, prefix="/api", tags=["execute"])
app.include_router(ai.router, prefix="/api/ai", tags=["ai"])
app.include_router(settings.router, prefix="/api", tags=["settings"])
app.include_router(os_info.router, prefix="/api", tags=["os_info"])

# 启动事件
@app.on_event("startup")
async def startup_event():
    """应用启动时的初始化操作"""
    setup_logging()
    logging.info("AI Terminal Assistant 启动")

# 关闭事件
@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时的清理操作"""
    logging.info("AI Terminal Assistant 关闭")

def main():
    """主入口函数"""
    try:
        # 初始化配置管理器（使用默认配置文件路径）
        config = ConfigManager()
        
        # 创建并启动Web服务器
        server = WebServer(config)
        server.start()
        
    except Exception as e:
        logger.error(f"启动失败: {str(e)}")
        raise

if __name__ == '__main__':
    main() 