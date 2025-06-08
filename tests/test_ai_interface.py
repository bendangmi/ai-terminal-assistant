"""
AI接口测试模块
"""

import os
import unittest
from unittest.mock import patch, MagicMock
from typing import Dict, Any

from ata.ai_interface import AIInterface, OpenAIProvider, DeepSeekProvider
from ata.exceptions import AIError, APIError

class TestAIInterface(unittest.TestCase):
    """测试AI接口基类"""
    
    def setUp(self):
        """测试前的准备工作"""
        self.ai_interface = AIInterface(
            provider="openai",
            model="gpt-3.5-turbo",
            api_key="test_key"
        )
    
    def test_initialization(self):
        """测试初始化"""
        self.assertEqual(self.ai_interface.provider, "openai")
        self.assertEqual(self.ai_interface.model, "gpt-3.5-turbo")
        self.assertEqual(self.ai_interface.api_key, "test_key")
    
    def test_provider_switching(self):
        """测试提供商切换"""
        self.ai_interface.switch_provider("deepseek")
        self.assertEqual(self.ai_interface.provider, "deepseek")
    
    def test_model_switching(self):
        """测试模型切换"""
        self.ai_interface.switch_model("gpt-4")
        self.assertEqual(self.ai_interface.model, "gpt-4")
    
    def test_temperature_setting(self):
        """测试温度设置"""
        self.ai_interface.set_temperature(0.8)
        self.assertEqual(self.ai_interface.temperature, 0.8)
    
    def test_invalid_provider(self):
        """测试无效提供商"""
        with self.assertRaises(ValueError):
            AIInterface(provider="invalid")
    
    def test_invalid_model(self):
        """测试无效模型"""
        with self.assertRaises(ValueError):
            AIInterface(provider="openai", model="invalid")
    
    def test_missing_api_key(self):
        """测试缺少API密钥"""
        with self.assertRaises(ValueError):
            AIInterface(provider="openai", api_key=None)

class TestOpenAIProvider(unittest.TestCase):
    """测试OpenAI提供商"""
    
    def setUp(self):
        """测试前的准备工作"""
        self.provider = OpenAIProvider(api_key="test_key")
    
    @patch("openai.ChatCompletion.create")
    def test_generate_command(self, mock_create):
        """测试生成命令"""
        # 模拟OpenAI API响应
        mock_create.return_value = MagicMock(
            choices=[
                MagicMock(
                    message=MagicMock(
                        content="""
                        {
                            "command": "ls -la",
                            "explanation": "List all files",
                            "warnings": []
                        }
                        """
                    )
                )
            ]
        )
        
        result = self.provider.generate_command(
            "list files",
            system_info={"os": "linux"}
        )
        
        self.assertEqual(result["command"], "ls -la")
        self.assertEqual(result["explanation"], "List all files")
        self.assertEqual(result["warnings"], [])
    
    @patch("openai.ChatCompletion.create")
    def test_api_error(self, mock_create):
        """测试API错误"""
        mock_create.side_effect = Exception("API Error")
        
        with self.assertRaises(APIError):
            self.provider.generate_command(
                "list files",
                system_info={"os": "linux"}
            )
    
    @patch("openai.ChatCompletion.create")
    def test_invalid_response(self, mock_create):
        """测试无效响应"""
        mock_create.return_value = MagicMock(
            choices=[
                MagicMock(
                    message=MagicMock(
                        content="Invalid JSON"
                    )
                )
            ]
        )
        
        with self.assertRaises(AIError):
            self.provider.generate_command(
                "list files",
                system_info={"os": "linux"}
            )

class TestDeepSeekProvider(unittest.TestCase):
    """测试DeepSeek提供商"""
    
    def setUp(self):
        """测试前的准备工作"""
        self.provider = DeepSeekProvider(api_key="test_key")
    
    @patch("deepseek.ChatCompletion.create")
    def test_generate_command(self, mock_create):
        """测试生成命令"""
        # 模拟DeepSeek API响应
        mock_create.return_value = MagicMock(
            choices=[
                MagicMock(
                    message=MagicMock(
                        content="""
                        {
                            "command": "ls -la",
                            "explanation": "List all files",
                            "warnings": []
                        }
                        """
                    )
                )
            ]
        )
        
        result = self.provider.generate_command(
            "list files",
            system_info={"os": "linux"}
        )
        
        self.assertEqual(result["command"], "ls -la")
        self.assertEqual(result["explanation"], "List all files")
        self.assertEqual(result["warnings"], [])
    
    @patch("deepseek.ChatCompletion.create")
    def test_api_error(self, mock_create):
        """测试API错误"""
        mock_create.side_effect = Exception("API Error")
        
        with self.assertRaises(APIError):
            self.provider.generate_command(
                "list files",
                system_info={"os": "linux"}
            )
    
    @patch("deepseek.ChatCompletion.create")
    def test_invalid_response(self, mock_create):
        """测试无效响应"""
        mock_create.return_value = MagicMock(
            choices=[
                MagicMock(
                    message=MagicMock(
                        content="Invalid JSON"
                    )
                )
            ]
        )
        
        with self.assertRaises(AIError):
            self.provider.generate_command(
                "list files",
                system_info={"os": "linux"}
            )

if __name__ == "__main__":
    unittest.main()
