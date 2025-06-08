import logging
import logging.config
import yaml
import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import router as api_router

# 配置日志
def setup_logging():
    """配置日志系统"""
    try:
        # 创建日志目录
        log_dir = Path(__file__).parent.parent / "logs"
        log_dir.mkdir(exist_ok=True)
        
        # 加载日志配置
        log_config_path = Path(__file__).parent / "config" / "logging.yaml"
        if log_config_path.exists():
            with open(log_config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
                
                # 确保日志文件路径存在
                if "file" in config.get("handlers", {}):
                    log_file = config["handlers"]["file"]["filename"]
                    if not os.path.isabs(log_file):
                        config["handlers"]["file"]["filename"] = str(log_dir / "ata.log")
                
                logging.config.dictConfig(config)
                logging.info(f"成功加载日志配置: {log_config_path}")
        else:
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            logging.warning(f"日志配置文件不存在: {log_config_path}，使用默认配置")
            
    except Exception as e:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        logging.error(f"配置日志系统失败: {str(e)}", exc_info=True)

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

# 注册API路由
app.include_router(api_router, prefix="/api")

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