"""API模块

包含所有API路由处理器。
"""

from fastapi import APIRouter
from . import os_info
from . import execute
from . import settings
from . import ai_execute

# 创建主路由器
router = APIRouter()

# 注册子路由器
router.include_router(os_info.router, prefix="/os-info", tags=["os_info"])
router.include_router(execute.router, prefix="/execute", tags=["execute"])
router.include_router(settings.router, prefix="/settings", tags=["settings"])
router.include_router(ai_execute.router, prefix="/ai", tags=["ai"]) 