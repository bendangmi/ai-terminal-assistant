"""
AI Terminal Assistant Web 服务器模块
"""

import os
import json
import logging
import html
import re
from typing import Optional, Dict, Any, List
from pathlib import Path
from datetime import datetime

from quart import Quart, request, jsonify, send_from_directory
from quart_cors import cors

from .ai_interface import AIInterface
from .command_executor import CommandExecutor
from .config_manager import ConfigManager
from .system_monitor import SystemMonitor

logger = logging.getLogger(__name__)

class WebServer:
    """Web服务器类"""
    
    def __init__(self, config: ConfigManager):
        """初始化Web服务器
        
        Args:
            config: 配置管理器实例
        """
        self.config = config
        self.app = Quart(__name__)
        
        # 添加CORS支持
        self.app = cors(self.app, allow_origin=["http://localhost:3000"])
        
        self.ai_interface = AIInterface(config)
        self.command_executor = CommandExecutor(config)
        self.system_monitor = SystemMonitor()
        
        # 获取项目根目录
        self.project_root = Path(__file__).parent.parent
        
        # 注册路由
        self._setup_routes()
    
    def _format_terminal_output(self, output: str, is_error: bool = False) -> Dict[str, Any]:
        """格式化终端输出
        
        Args:
            output: 原始输出文本
            is_error: 是否是错误输出
            
        Returns:
            格式化后的输出数据
        """
        if not output:
            return {
                "type": "error" if is_error else "output",
                "content": "",
                "timestamp": datetime.now().isoformat()
            }
            
        # 转义HTML特殊字符
        output = html.escape(output)
        
        # 处理ANSI颜色代码
        ansi_colors = {
            '\x1b[30m': 'color: black;',
            '\x1b[31m': 'color: red;',
            '\x1b[32m': 'color: green;',
            '\x1b[33m': 'color: yellow;',
            '\x1b[34m': 'color: blue;',
            '\x1b[35m': 'color: magenta;',
            '\x1b[36m': 'color: cyan;',
            '\x1b[37m': 'color: white;',
            '\x1b[0m': ''
        }
        
        for ansi, css in ansi_colors.items():
            output = output.replace(ansi, f'</span><span style="{css}">' if css else '</span>')
        
        # 处理换行符
        output = output.replace('\n', '<br/>')
        
        # 处理制表符
        output = output.replace('\t', '&nbsp;&nbsp;&nbsp;&nbsp;')
        
        # 处理多个空格
        output = re.sub(r' {2,}', lambda m: '&nbsp;' * len(m.group()), output)
        
        return {
            "type": "error" if is_error else "output",
            "content": f'<span>{output}</span>',
            "timestamp": datetime.now().isoformat()
        }
    
    def _setup_routes(self):
        """设置路由"""
        
        @self.app.route('/')
        async def index():
            web_dir = self.project_root / 'web'
            return await send_from_directory(web_dir, 'index.html')
        
        @self.app.route('/<path:path>')
        async def static_files(path):
            web_dir = self.project_root / 'web'
            return await send_from_directory(web_dir, path)
        
        @self.app.route('/api/status')
        async def status():
            return jsonify({
                "status": "running",
                "version": self.config.get("version"),
                "ai_provider": self.config.get("ai.provider"),
                "model": self.config.get(f"ai.{self.config.get('ai.provider')}.model")
            })

        @self.app.route('/api/settings', methods=['GET'])
        async def get_settings():
            """获取当前设置"""
            try:
                settings = {
                    "ai": {
                        "provider": self.config.get("ai.provider"),
                        "model": self.config.get(f"ai.{self.config.get('ai.provider')}.model"),
                        "temperature": self.config.get(f"ai.{self.config.get('ai.provider')}.temperature"),
                        "api_key": self.config.get(f"ai.{self.config.get('ai.provider')}.api_key", "")
                    },
                    "system": {
                        "updateInterval": self.config.get("general.history_size", 20),
                        "logLevel": self.config.get("logging.level", "INFO"),
                        "autoStart": self.config.get("general.auto_start", False)
                    },
                    "terminal": {
                        "fontSize": self.config.get("ui.terminal.font_size", 14),
                        "fontFamily": self.config.get("ui.terminal.font_family", "Consolas"),
                        "theme": self.config.get("ui.terminal.theme", "dark"),
                        "historySize": self.config.get("ui.terminal.history_size", 100)
                    }
                }
                return jsonify(settings)
            except Exception as e:
                logger.error(f"获取设置失败: {str(e)}")
                return jsonify({"error": str(e)}), 500

        @self.app.route('/api/settings', methods=['POST'])
        async def update_settings():
            """更新设置"""
            try:
                data = await request.get_json()
                
                # 更新AI配置
                if "ai" in data:
                    ai_config = data["ai"]
                    provider = ai_config.get("provider")
                    if provider:
                        self.config.set("ai.provider", provider)
                        self.config.set(f"ai.{provider}.model", ai_config.get("model"))
                        self.config.set(f"ai.{provider}.temperature", float(ai_config.get("temperature", 0.7)))
                        if ai_config.get("api_key"):
                            self.config.set(f"ai.{provider}.api_key", ai_config["api_key"])
                
                # 更新系统配置
                if "system" in data:
                    sys_config = data["system"]
                    self.config.set("general.history_size", sys_config.get("updateInterval", 20))
                    self.config.set("logging.level", sys_config.get("logLevel", "INFO"))
                    self.config.set("general.auto_start", sys_config.get("autoStart", False))
                
                # 更新终端配置
                if "terminal" in data:
                    term_config = data["terminal"]
                    self.config.set("ui.terminal.font_size", term_config.get("fontSize", 14))
                    self.config.set("ui.terminal.font_family", term_config.get("fontFamily", "Consolas"))
                    self.config.set("ui.terminal.theme", term_config.get("theme", "dark"))
                    self.config.set("ui.terminal.history_size", term_config.get("historySize", 100))
                
                # 保存配置
                self.config.save()
                
                # 重新初始化AI接口
                self.ai_interface = AIInterface(self.config)
                
                return jsonify({"status": "success"})
            except Exception as e:
                logger.error(f"更新设置失败: {str(e)}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/execute-raw', methods=['POST'])
        async def execute_raw():
            """直接执行原始命令"""
            try:
                data = await request.get_json()
                command = data.get("command")
                if not command:
                    return jsonify({"error": "命令不能为空"}), 400
                
                # 检查命令安全性
                is_dangerous, warnings = self.command_executor.is_dangerous(command)
                if is_dangerous and not data.get("force", False):
                    return jsonify({
                        "error": "危险命令",
                        "warnings": warnings,
                        "output": [{
                            "type": "error",
                            "content": f"<span>警告: {warning}</span>",
                            "timestamp": datetime.now().isoformat()
                        } for warning in warnings]
                    }), 400
                
                # 执行命令
                result = self.command_executor.execute(command)
                
                # 格式化输出
                formatted_output = []
                
                if result.stdout:
                    formatted_output.append(self._format_terminal_output(result.stdout))
                    
                if result.stderr:
                    formatted_output.append(self._format_terminal_output(result.stderr, is_error=True))
                
                # 添加执行状态
                formatted_output.append({
                    "type": "status",
                    "content": f"<span>命令{'成功' if result.success else '失败'} (退出代码: {result.exit_code}, 耗时: {result.duration:.2f}s)</span>",
                    "timestamp": datetime.now().isoformat()
                })
                
                return jsonify({
                    "success": result.success,
                    "output": formatted_output,
                    "exit_code": result.exit_code,
                    "duration": result.duration
                })
                
            except Exception as e:
                logger.error(f"执行原始命令失败: {str(e)}")
                return jsonify({
                    "error": str(e),
                    "output": [{
                        "type": "error",
                        "content": f"<span>执行出错: {str(e)}</span>",
                        "timestamp": datetime.now().isoformat()
                    }]
                }), 400
        
        @self.app.route('/api/execute', methods=['POST'])
        async def execute():
            """通过AI执行命令"""
            try:
                data = await request.get_json()
                user_input = data.get("command")
                if not user_input:
                    return jsonify({"error": "命令不能为空"}), 400

                # 首先通过AI接口处理自然语言输入
                try:
                    command = await self.ai_interface.chat(user_input)
                    logger.info(f"AI转换结果 - 输入: {user_input}, 输出: {command}")
                except Exception as e:
                    logger.error(f"AI处理失败: {str(e)}")
                    return jsonify({
                        "error": f"AI无法理解您的输入: {str(e)}",
                        "output": [{
                            "type": "error",
                            "content": f"<span>AI处理失败: {str(e)}</span>",
                            "timestamp": datetime.now().isoformat()
                        }]
                    }), 400

                # 显示AI转换的命令
                formatted_output = [{
                    "type": "info",
                    "content": f"<span>转换后的命令: {command}</span>",
                    "timestamp": datetime.now().isoformat()
                }]
                
                # 检查命令安全性
                is_dangerous, warnings = self.command_executor.is_dangerous(command)
                if is_dangerous and not data.get("force", False):
                    return jsonify({
                        "error": "危险命令",
                        "warnings": warnings,
                        "output": formatted_output + [{
                            "type": "error",
                            "content": f"<span>警告: {warning}</span>",
                            "timestamp": datetime.now().isoformat()
                        } for warning in warnings]
                    }), 400
                
                # 执行命令
                result = self.command_executor.execute(command)
                
                # 添加命令输出
                if result.stdout:
                    formatted_output.append(self._format_terminal_output(result.stdout))
                    
                if result.stderr:
                    formatted_output.append(self._format_terminal_output(result.stderr, is_error=True))
                
                # 添加执行状态
                formatted_output.append({
                    "type": "status",
                    "content": f"<span>命令{'成功' if result.success else '失败'} (退出代码: {result.exit_code}, 耗时: {result.duration:.2f}s)</span>",
                    "timestamp": datetime.now().isoformat()
                })

                return jsonify({
                    "success": result.success,
                    "output": formatted_output,
                    "exit_code": result.exit_code,
                    "duration": result.duration
                })
                
            except Exception as e:
                logger.error(f"处理执行请求时出错: {str(e)}")
                return jsonify({
                    "error": str(e),
                    "output": [{
                        "type": "error",
                        "content": f"<span>执行出错: {str(e)}</span>",
                        "timestamp": datetime.now().isoformat()
                    }]
                }), 400
        
        @self.app.route('/api/history')
        async def history():
            try:
                history = self.ai_interface.get_history()
                return jsonify({"history": history})
            except Exception as e:
                logger.error(f"处理历史记录请求时出错: {str(e)}")
                return jsonify({"error": str(e)}), 400

        @self.app.route('/api/test-connection', methods=['POST'])
        async def test_connection():
            """测试服务器连接"""
            try:
                data = await request.get_json()
                host = data.get("host", "")
                port = data.get("port", "")
                
                if not host or not port:
                    return jsonify({"error": "主机和端口不能为空"}), 400
                
                # 尝试连接
                import socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)  # 设置超时时间为5秒
                
                try:
                    sock.connect((host, int(port)))
                    sock.close()
                    return jsonify({"status": "success", "message": "连接成功"})
                except Exception as e:
                    return jsonify({"status": "error", "message": f"连接失败: {str(e)}"})
                
            except Exception as e:
                logger.error(f"测试连接失败: {str(e)}")
                return jsonify({"error": str(e)}), 400

        @self.app.route('/api/test-ai-config', methods=['POST'])
        async def test_ai_config():
            """测试AI配置"""
            try:
                data = await request.get_json()
                provider = data.get("provider")
                api_key = data.get("apiKey")
                model = data.get("model")
                
                if not all([provider, api_key, model]):
                    return jsonify({"error": "所有配置项都不能为空"}), 400
                
                # 创建临时配置进行测试
                test_config = ConfigManager(self.config.config_file)
                test_config.set(f"ai.{provider}.api_key", api_key)
                test_config.set(f"ai.{provider}.model", model)
                test_config.set("ai.provider", provider)
                
                # 创建临时AI接口实例进行测试
                try:
                    test_ai = AIInterface(test_config)
                    # 发送测试请求
                    response = await test_ai.chat("测试消息")
                    return jsonify({
                        "status": "success",
                        "message": "AI配置测试成功",
                        "response": response
                    })
                except Exception as e:
                    return jsonify({
                        "status": "error",
                        "message": f"AI配置测试失败: {str(e)}"
                    })
                
            except Exception as e:
                logger.error(f"测试AI配置失败: {str(e)}")
                return jsonify({"error": str(e)}), 400

        @self.app.route('/api/system-info')
        async def system_info():
            """获取系统信息"""
            try:
                info = self.system_monitor.get_system_info()
                return jsonify(info)
            except Exception as e:
                logger.error(f"获取系统信息失败: {str(e)}")
                return jsonify({"error": str(e)}), 400

        @self.app.route('/api/ai/execute', methods=['POST'])
        async def ai_execute():
            """执行AI命令"""
            try:
                data = await request.get_json()
                command = data.get("command")
                if not command:
                    return jsonify({"error": "命令不能为空"}), 400
                
                response = await self.ai_interface.chat(command)
                return jsonify({"response": response})
            except Exception as e:
                logger.error(f"执行AI命令失败: {str(e)}")
                return jsonify({"error": str(e)}), 500
    
    def start(self):
        """启动Web服务器"""
        host = self.config.get("general.web_server.host", "127.0.0.1")
        port = self.config.get("general.web_server.port", 8000)
        debug = self.config.get("general.web_server.debug", False)
        
        logger.info(f"启动Web服务器: http://{host}:{port}")
        self.app.run(host=host, port=port, debug=debug) 