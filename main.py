from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ata.api import router as api_router
import uvicorn
import argparse
import socket
from contextlib import closing

app = FastAPI(title="AI Terminal Assistant")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置为具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册API路由
app.include_router(api_router, prefix="/api")

def find_free_port(start_port=8000, max_port=9000):
    """查找可用端口"""
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        port = start_port
        while port < max_port:
            try:
                sock.bind(('127.0.0.1', port))
                return port
            except socket.error:
                port += 1
    raise IOError('找不到可用的端口')

def main():
    parser = argparse.ArgumentParser(description='AI Terminal Assistant 服务器')
    parser.add_argument('--host', default='127.0.0.1', help='监听地址 (默认: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=8000, help='监听端口 (默认: 8000)')
    parser.add_argument('--reload', action='store_true', help='启用热重载 (开发模式)')
    parser.add_argument('--workers', type=int, default=1, help='工作进程数 (默认: 1)')
    args = parser.parse_args()

    try:
        # 如果指定端口被占用，尝试找到可用端口
        if args.port == 8000:
            try:
                with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
                    sock.bind((args.host, args.port))
            except socket.error:
                print(f"警告: 端口 {args.port} 已被占用，尝试查找可用端口...")
                args.port = find_free_port()
                print(f"使用新端口: {args.port}")

        # 启动服务器
        uvicorn.run(
            "ata.app:app",
            host=args.host,
            port=args.port,
            reload=args.reload,
            workers=args.workers if not args.reload else 1,  # 热重载模式下只能使用单进程
            log_config="ata/config/logging.yaml"
        )
    except Exception as e:
        print(f"启动服务器时发生错误: {str(e)}")
        return 1

if __name__ == "__main__":
    main() 