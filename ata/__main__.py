"""
AI Terminal Assistant主程序入口
"""

import os
import sys
import logging
import argparse
import asyncio
from pathlib import Path
from typing import Optional

from rich.logging import RichHandler

from .config_manager import ConfigManager
from .command_executor import CommandExecutor
from .ai_interface import AIInterface
from .cli import CLI
from .web_server import WebServer


logger = logging.getLogger(__name__)


def setup_logging(config: ConfigManager) -> None:
    """设置日志记录
    
    Args:
        config: 配置管理器实例
    """
    log_level = config.get("logging.level", "INFO")
    log_format = config.get("logging.format", "%(message)s")
    log_file = config.get("logging.file")
    
    # 设置Rich日志处理器
    rich_handler = RichHandler(
        rich_tracebacks=True,
        markup=True,
        show_time=False,
        show_path=False
    )
    
    # 如果指定了日志文件，同时输出到文件
    handlers = [rich_handler]
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter(
            config.get("logging.format"),
            datefmt=config.get("logging.date_format")
        ))
        handlers.append(file_handler)
    
    # 配置根日志记录器
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format,
        handlers=handlers,
        force=True
    )


def parse_args() -> argparse.Namespace:
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="AI Terminal Assistant - 智能终端助手",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "--config",
        type=str,
        help="配置文件路径"
    )
    
    parser.add_argument(
        "--provider",
        choices=["openai", "deepseek"],
        help="AI提供商"
    )
    
    parser.add_argument(
        "--model",
        type=str,
        help="AI模型名称"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="启用调试模式"
    )
    
    parser.add_argument(
        "--working-dir",
        type=str,
        help="工作目录"
    )
    
    parser.add_argument(
        "--web",
        action="store_true",
        help="启用Web模式"
    )
    
    parser.add_argument(
        "query",
        nargs="*",
        help="要执行的查询"
    )
    
    return parser.parse_args()


async def async_main(args: Optional[argparse.Namespace] = None) -> int:
    """异步主函数
    
    Args:
        args: 命令行参数

    Returns:
        退出代码
    """
    if args is None:
        args = parse_args()
    
    try:
        # 创建配置管理器
        config_path = args.config if args and args.config else "config.yaml"
        config = ConfigManager(Path(config_path))
        
        # 设置日志记录
        setup_logging(config)
        
        # 强制设置为 deepseek
        config.set("ai.provider", "deepseek")
        
        # 如果指定了参数，更新配置
        if args.provider:
            config.set("ai.provider", args.provider)
        if args.model:
            config.set(f"ai.{config.get('ai.provider')}.model", args.model)
        if args.debug:
            config.set("general.debug_mode", True)
        if args.working_dir:
            config.set("general.working_directory", args.working_dir)
        
        # 创建组件
        ai_interface = AIInterface(config)
        command_executor = CommandExecutor(config)
        
        try:
            # 根据模式选择运行方式
            if args.web or config.get("general.web_server.enabled", False):
                # Web模式
                web_server = WebServer(config)
                host = config.get("general.web_server.host", "127.0.0.1")
                port = config.get("general.web_server.port", 8000)
                debug = config.get("general.web_server.debug", False)
                
                logger.info(f"启动Web服务器: http://{host}:{port}")
                await web_server.app.run_task(host=host, port=port, debug=debug)
                    
            else:
                # CLI模式
                cli = CLI(ai_interface, command_executor, config)
                
                # 如果提供了查询，直接执行
                if args.query:
                    query = " ".join(args.query)
                    await cli.process_user_input(query)
                    return 0
                
                # 否则进入交互模式
                return await cli.run()
            
            return 0
            
        finally:
            # 确保关闭所有资源
            await ai_interface.close()
        
    except KeyboardInterrupt:
        print("\n程序已中断")
        return 1
    except Exception as e:
        logging.error(f"运行时出错: {str(e)}", exc_info=True)
        return 1


def main(args: Optional[argparse.Namespace] = None) -> int:
    """主函数入口
    
    Args:
        args: 命令行参数

    Returns:
        退出代码
    """
    try:
        if os.name == 'nt':  # Windows
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        return asyncio.run(async_main(args))
    except Exception as e:
        logging.error(f"运行时出错: {str(e)}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main()) 