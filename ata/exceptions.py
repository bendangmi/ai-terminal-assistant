"""
异常类模块
"""

class ATAError(Exception):
    """AI终端助手基础异常类"""
    pass


class AIError(ATAError):
    """AI服务相关错误"""
    pass


class APIError(AIError):
    """API调用错误"""
    pass


class CommandExecutionError(ATAError):
    """命令执行错误"""
    pass


class SecurityError(ATAError):
    """安全相关错误"""
    pass


class ConfigError(ATAError):
    """配置相关错误"""
    pass 