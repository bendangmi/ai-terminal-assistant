#!/usr/bin/env python3
"""
AI终端助手端到端测试脚本

这个脚本使用mock来模拟AI接口和命令执行，以便进行端到端测试。
支持测试不同的模型提供商（OpenAI和DeepSeek）。
"""

import os
import sys
import argparse
import unittest
import asyncio
from unittest.mock import patch, MagicMock
from pathlib import Path
import tempfile
import logging

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from ata.ai_interface import AIInterface, OpenAIProvider, DeepSeekProvider
from ata.command_executor import CommandExecutor
from ata.cli import CLI
from ata.config_manager import ConfigManager
from ata.exceptions import AIError, APIError


def mock_generate_command(*args, **kwargs):
    """模拟AI生成命令的函数"""
    return {
        "command": "echo 'Hello World'",
        "explanation": "这是一个测试命令",
        "warnings": []
    }


def mock_execute_command(*args, **kwargs):
    """模拟执行命令的函数"""
    return {
        "success": True,
        "exit_code": 0,
        "stdout": "Hello World",
        "stderr": "",
        "duration": 0.1
    }


async def mock_openai_fail(*args, **kwargs):
    """模拟OpenAI API调用失败"""
    raise APIError("OpenAI API调用失败")


async def mock_deepseek_success(*args, **kwargs):
    """模拟DeepSeek API调用成功"""
    return {
        "command": "echo 'Success from DeepSeek'",
        "explanation": "这是一个来自DeepSeek的测试命令",
        "warnings": []
    }


class TestMockExample(unittest.TestCase):
    """使用mock进行单元测试的示例类"""
    
    def setUp(self):
        """测试前的准备工作"""
        # 创建临时配置文件
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, "config.yaml")
        
        # 初始化配置管理器
        self.config = ConfigManager(self.config_path)
        
        # 设置测试配置
        self.config.set("ai.provider", "openai")
        self.config.set("ai.openai.api_key", "mock_api_key")
        self.config.set("ai.openai.model", "gpt-3.5-turbo")
        self.config.set("ai.deepseek.api_key", "mock_api_key")
        self.config.set("ai.deepseek.model", "deepseek-chat")
        self.config.save_config()
        
        # 初始化命令执行器
        self.executor = CommandExecutor(self.config)
        
        # 设置事件循环
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
    
    def tearDown(self):
        """测试后的清理工作"""
        # 清理临时文件
        import shutil
        shutil.rmtree(self.temp_dir)
        
        # 清理事件循环
        self.loop.close()
    
    def test_mock_command_generation(self):
        """测试使用mock生成命令"""
        # 使用mock替换真实的API调用
        with patch.object(OpenAIProvider, 'generate_command', side_effect=mock_generate_command):
            # 创建AI接口实例
            ai_interface = AIInterface(config=self.config)
            
            # 生成命令
            result = self.loop.run_until_complete(
                ai_interface._provider.generate_command(
                    "测试命令",
                    system_info={"os": "test"}
                )
            )
            
            # 验证结果
            self.assertEqual(result["command"], "echo 'Hello World'")
            self.assertEqual(result["explanation"], "这是一个测试命令")
            self.assertEqual(result["warnings"], [])
            
            # 执行命令
            exec_result = self.executor.execute(result["command"])
            
            # 验证执行结果
            self.assertTrue(exec_result.success)
            self.assertEqual(exec_result.stdout, "Hello World")
    
    def test_mock_fallback(self):
        """测试使用mock测试故障转移"""
        # 设置故障转移配置
        self.config.set("ai.fallback_provider", "deepseek")
        self.config.save_config()
        
        # 使用mock模拟OpenAI失败和DeepSeek成功的情况
        with patch.object(OpenAIProvider, 'generate_command', side_effect=mock_openai_fail), \
             patch.object(DeepSeekProvider, 'generate_command', side_effect=mock_deepseek_success):
            
            # 创建只有OpenAI的实例（应该失败）
            ai_interface = AIInterface(config=self.config)
            
            # 这应该会失败
            with self.assertRaises(APIError):
                self.loop.run_until_complete(
                    ai_interface.generate_command(
                        "测试命令",
                        system_info={"os": "test"}
                    )
                )
            
            # 使用DeepSeek作为故障转移
            ai_interface = AIInterface(
                config=self.config,
                fallback_provider="deepseek"
            )
            
            # 这应该会成功（使用DeepSeek）
            result = self.loop.run_until_complete(
                ai_interface.generate_command(
                    "测试命令",
                    system_info={"os": "test"}
                )
            )
            
            # 验证结果来自DeepSeek
            self.assertEqual(
                result["command"],
                "echo 'Success from DeepSeek'"
            )


def mock_execute(self, command, timeout=30):
    """模拟命令执行器的execute方法"""
    print(f"模拟执行命令: {command}")
    
    # 根据命令返回不同的结果
    if command == "ls -la":
        return {
            "success": True,
            "exit_code": 0,
            "stdout": "total 16\ndrwxr-xr-x 2 user user 4096 Jun 7 12:00 .\ndrwxr-xr-x 3 user user 4096 Jun 7 12:00 ..\n-rw-r--r-- 1 user user  123 Jun 7 12:00 file1.txt\n-rw-r--r-- 1 user user  456 Jun 7 12:00 file2.txt",
            "stderr": "",
            "duration": 0.1,
        }
    elif command == "free -h":
        return {
            "success": True,
            "exit_code": 0,
            "stdout": "              total        used        free      shared  buff/cache   available\nMem:           15Gi       5.0Gi       2.0Gi       1.0Gi       8.0Gi       9.0Gi\nSwap:          2.0Gi       0.0Gi       2.0Gi",
            "stderr": "",
            "duration": 0.1,
        }
    elif "echo" in command:
        output = command.split("'")[1] if "'" in command else command.split('"')[1]
        return {
            "success": True,
            "exit_code": 0,
            "stdout": output,
            "stderr": "",
            "duration": 0.1,
        }
    else:
        return {
            "success": False,
            "exit_code": 1,
            "stdout": "",
            "stderr": "命令执行失败",
            "duration": 0.1,
        }


def mock_is_dangerous(self, command):
    """模拟命令执行器的is_dangerous方法"""
    if "rm -rf /" in command:
        return True, ["命令尝试删除根目录"]
    elif "sudo" in command:
        return True, ["命令包含权限提升操作"]
    else:
        return False, []


def mock_input(prompt=""):
    """模拟用户输入"""
    print(prompt, end="")
    # 始终返回"y"表示确认执行
    print(" y")
    return "y"


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="运行AI终端助手的端到端测试")
    parser.add_argument("--verbose", "-v", action="store_true", help="显示详细输出")
    args = parser.parse_args()
    
    # 设置日志级别
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    
    # 运行测试
    unittest.main(argv=[sys.argv[0]])


if __name__ == "__main__":
    main()

