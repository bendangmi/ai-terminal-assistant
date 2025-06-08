"""
AI接口模块，提供与不同AI提供商的交互功能
"""

import os
import json
import logging
import asyncio
import socket
import sys
from typing import Dict, Any, List, Optional, Generator, Union, AsyncGenerator
from pathlib import Path

import openai
from openai import OpenAI
import aiohttp
import requests
from aiohttp import ClientTimeout, TCPConnector
from pydantic import BaseModel, Field

# 网络配置
DEFAULT_TIMEOUT = 30  # 默认超时时间（秒）
MAX_RETRIES = 3      # 最大重试次数
RETRY_DELAY = 1      # 重试延迟（秒）

from .config_manager import ConfigManager
from .exceptions import AIError, APIError

logger = logging.getLogger(__name__)


class Message(BaseModel):
    """对话消息模型"""
    role: str = Field(..., description="消息角色（user/assistant/system）")
    content: str = Field(..., description="消息内容")


class AIProvider:
    """AI提供商基类"""
    
    DEFAULT_MODEL = None  # 子类必须定义默认模型
    
    def __init__(self, api_key: str, model: str, temperature: float = 0.7):
        """初始化AI提供商
        
        Args:
            api_key: API密钥
            model: 模型名称
            temperature: 温度参数
        """
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
    
    async def generate_command(self, 
                             user_input: str,
                             system_info: Dict[str, Any],
                             history: Optional[List[Dict[str, str]]] = None
                             ) -> Dict[str, Any]:
        """生成命令
        
        Args:
            user_input: 用户输入
            system_info: 系统信息
            history: 历史记录
            
        Returns:
            包含命令和解释的字典
            
        Raises:
            AIError: AI服务错误
            APIError: API调用错误
        """
        raise NotImplementedError
    
    async def stream_chat(self, 
                         messages: List[Dict[str, str]],
                         system_info: Dict[str, Any]
                         ) -> AsyncGenerator[str, None]:
        """流式聊天
        
        Args:
            messages: 消息列表
            system_info: 系统信息
            
        Returns:
            聊天响应生成器
            
        Raises:
            AIError: AI服务错误
            APIError: API调用错误
        """
        raise NotImplementedError


class OpenAIProvider(AIProvider):
    """OpenAI提供商实现"""
    
    DEFAULT_MODEL = "gpt-3.5-turbo"  # OpenAI的默认模型
    
    def __init__(self, api_key: str, model: Optional[str] = None, temperature: float = 0.7):
        """初始化OpenAI提供商
        
        Args:
            api_key: API密钥
            model: 模型名称，如果未指定则使用默认模型
            temperature: 温度参数
        """
        super().__init__(api_key, model or self.DEFAULT_MODEL, temperature)
        self.client = OpenAI(api_key=api_key)
    
    async def generate_command(self,
                             user_input: str,
                             system_info: Dict[str, Any],
                             history: Optional[List[Dict[str, str]]] = None
                             ) -> Dict[str, Any]:
        """生成命令
        
        Args:
            user_input: 用户输入
            system_info: 系统信息
            history: 历史记录
            
        Returns:
            包含命令和解释的字典
            
        Raises:
            APIError: API调用错误
            AIError: AI服务错误
        """
        try:
            messages = []
            
            # 添加系统信息
            messages.append({
                "role": "system",
                "content": """你是一个命令行助手。你的任务是将用户的自然语言输入转换为具体的命令。
你必须以JSON格式返回响应，格式如下：
{
    "command": "具体的命令",
    "explanation": "命令的解释",
    "warnings": ["可能的风险提示"]
}

系统信息：""" + json.dumps(system_info)
            })
            
            # 添加历史记录
            if history:
                messages.extend(history)
            
            # 添加用户输入
            messages.append({
                "role": "user",
                "content": user_input
            })
            
            # 调用API
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature
            )
            
            # 解析响应
            content = response.choices[0].message.content
            try:
                result = json.loads(content)
                return {
                    "command": result["command"],
                    "explanation": result["explanation"],
                    "warnings": result.get("warnings", [])
                }
            except (json.JSONDecodeError, KeyError) as e:
                raise AIError(f"无效的AI响应格式: {str(e)}")
            
        except Exception as e:
            if isinstance(e, AIError):
                raise
            raise APIError(f"OpenAI API调用失败: {str(e)}")
    
    async def stream_chat(self,
                         messages: List[Dict[str, str]],
                         system_info: Dict[str, Any]
                         ) -> AsyncGenerator[str, None]:
        """流式聊天
        
        Args:
            messages: 消息列表
            system_info: 系统信息
            
        Returns:
            聊天响应生成器
            
        Raises:
            APIError: API调用错误
        """
        try:
            # 添加系统信息
            all_messages = [
                {
                    "role": "system",
                    "content": """你是一个命令行助手。你的任务是将用户的自然语言输入转换为具体的命令。
你必须以JSON格式返回响应，格式如下：
{
    "command": "具体的命令",
    "explanation": "命令的解释",
    "warnings": ["可能的风险提示"]
}

系统信息：""" + json.dumps(system_info)
                }
            ]
            all_messages.extend(messages)
            
            # 调用流式API
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=all_messages,
                temperature=self.temperature,
                stream=True
            )
            
            async for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            raise APIError(f"OpenAI流式API调用失败: {str(e)}")


class DeepSeekProvider(AIProvider):
    """DeepSeek提供商实现"""
    
    API_URL = "https://api.deepseek.com/v1/chat/completions"  # 更新为正确的API端点
    DEFAULT_MODEL = "deepseek-chat"  # DeepSeek的默认模型
    
    def __init__(self, api_key: str, model: Optional[str] = None, temperature: float = 0.7):
        """初始化DeepSeek提供商
        
        Args:
            api_key: API密钥
            model: 模型名称，如果未指定则使用默认模型
            temperature: 温度参数
        """
        super().__init__(api_key, model or self.DEFAULT_MODEL, temperature)
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self._session = None
    
    @property
    async def session(self) -> aiohttp.ClientSession:
        """获取或创建aiohttp会话"""
        if self._session is None or self._session.closed:
            # 配置SSL和超时
            timeout = ClientTimeout(total=DEFAULT_TIMEOUT)
            connector = TCPConnector(
                ssl=False,  # 禁用SSL验证以处理某些证书问题
                force_close=True,  # 强制关闭连接以避免连接池问题
                enable_cleanup_closed=True,  # 清理已关闭的连接
                ttl_dns_cache=300,  # DNS缓存时间（秒）
            )
            self._session = aiohttp.ClientSession(
                headers=self.headers,
                timeout=timeout,
                connector=connector
            )
        return self._session
    
    async def close(self):
        """关闭会话"""
        if self._session and not self._session.closed:
            await self._session.close()
    
    async def _make_request(self, url: str, data: Dict[str, Any], retry_count: int = 0) -> Dict[str, Any]:
        """发送请求并处理重试逻辑
        
        Args:
            url: API端点URL
            data: 请求数据
            retry_count: 当前重试次数
            
        Returns:
            API响应数据
            
        Raises:
            APIError: API调用失败
        """
        try:
            session = await self.session
            async with session.post(url, json=data) as response:
                response_text = await response.text()
                logger.debug(f"API响应状态码: {response.status}")
                logger.debug(f"API原始响应: {response_text}")
                
                if response.status != 200:
                    raise APIError(f"DeepSeek API调用失败: {response.status} - {response_text}")
                
                return json.loads(response_text)
                
        except (aiohttp.ClientError, socket.gaierror, asyncio.TimeoutError) as e:
            if retry_count < MAX_RETRIES:
                logger.warning(f"API请求失败，将在{RETRY_DELAY}秒后重试 ({retry_count + 1}/{MAX_RETRIES}): {str(e)}")
                await asyncio.sleep(RETRY_DELAY)
                return await self._make_request(url, data, retry_count + 1)
            else:
                logger.error(f"API请求在{MAX_RETRIES}次重试后仍然失败: {str(e)}")
                raise APIError(f"DeepSeek API调用失败: {str(e)}")
        except Exception as e:
            logger.error(f"API请求出现未预期的错误: {str(e)}", exc_info=True)
            raise APIError(f"DeepSeek API调用失败: {str(e)}")
    
    def _clean_json_response(self, content: str) -> str:
        """清理JSON响应，处理可能的Markdown格式
        
        Args:
            content: AI响应内容
            
        Returns:
            清理后的JSON字符串
        """
        # 移除开头的空白字符
        content = content.strip()
        
        # 处理Markdown代码块
        if content.startswith("```") and content.endswith("```"):
            # 移除第一行（```json 或类似标记）
            lines = content.split("\n")
            # 移除最后一行（```）
            content = "\n".join(lines[1:-1])
        
        # 移除可能存在的制表符和多余的空格
        content = content.strip()
        
        logger.debug(f"清理后的JSON响应: {content}")
        return content

    async def generate_command(self,
                             user_input: str,
                             system_info: Dict[str, Any],
                             history: Optional[List[Dict[str, str]]] = None
                             ) -> Dict[str, Any]:
        """生成命令
        
        Args:
            user_input: 用户输入
            system_info: 系统信息
            history: 历史记录
            
        Returns:
            包含命令和解释的字典
            
        Raises:
            APIError: API调用错误
            AIError: AI服务错误
        """
        try:
            messages = []
            
            # 添加系统信息
            system_message = {
                "role": "system",
                "content": f"""你是一个命令行助手。你的任务是将用户的自然语言输入转换为具体的命令。
你必须以JSON格式返回响应，格式如下：
{{
    "commands": [
        {{
            "os": "windows",
            "command": "Windows系统下的命令",
            "explanation": "命令的解释"
        }},
        {{
            "os": "linux",
            "command": "Linux系统下的命令",
            "explanation": "命令的解释"
        }},
        {{
            "os": "darwin",
            "command": "MacOS系统下的命令",
            "explanation": "命令的解释"
        }}
    ],
    "warnings": ["可能的风险提示"]
}}

当前系统信息：
- 操作系统：{os.name} ({sys.platform})
- Python版本：{sys.version}

其他系统信息：{json.dumps(system_info)}"""
            }
            messages.append(system_message)
            logger.debug(f"系统提示: {system_message['content']}")
            
            # 添加历史记录
            if history:
                messages.extend(history)
                logger.debug(f"历史记录: {json.dumps(history, ensure_ascii=False)}")
            
            # 添加用户输入
            user_message = {
                "role": "user",
                "content": user_input
            }
            messages.append(user_message)
            logger.debug(f"用户输入: {user_input}")
            
            # 调用API
            data = {
                "model": self.model,
                "messages": messages,
                "temperature": self.temperature
            }
            logger.debug(f"API请求数据: {json.dumps(data, ensure_ascii=False)}")
            
            # 发送请求
            result = await self._make_request(self.API_URL, data)
            content = result["choices"][0]["message"]["content"]
            logger.debug(f"AI响应内容: {content}")
            
            try:
                # 清理响应内容
                cleaned_content = self._clean_json_response(content)
                command_data = json.loads(cleaned_content)
                logger.info(f"解析后的命令: {json.dumps(command_data, ensure_ascii=False)}")
                
                # 根据当前操作系统选择合适的命令
                current_os = sys.platform
                selected_command = None
                
                # 查找当前操作系统的命令
                for cmd in command_data["commands"]:
                    if current_os.startswith(cmd["os"]):
                        selected_command = cmd
                        break
                
                if not selected_command:
                    # 如果没有找到完全匹配的，尝试使用通用命令
                    if current_os.startswith("win"):
                        os_key = "windows"
                    elif current_os.startswith("linux"):
                        os_key = "linux"
                    elif current_os.startswith("darwin"):
                        os_key = "darwin"
                    else:
                        os_key = "linux"  # 默认使用Linux命令
                    
                    for cmd in command_data["commands"]:
                        if cmd["os"] == os_key:
                            selected_command = cmd
                            break
                
                if not selected_command:
                    raise AIError(f"未找到适用于当前操作系统({current_os})的命令")
                
                return {
                    "command": selected_command["command"],
                    "explanation": selected_command["explanation"],
                    "warnings": command_data.get("warnings", [])
                }
            except (json.JSONDecodeError, KeyError) as e:
                logger.error(f"AI响应格式无效: {content}")
                raise AIError(f"无效的AI响应格式: {str(e)}")
            
        except Exception as e:
            if isinstance(e, (AIError, APIError)):
                raise
            logger.error(f"生成命令时出错: {str(e)}", exc_info=True)
            raise APIError(f"DeepSeek API调用失败: {str(e)}")
    
    async def _make_stream_request(self, url: str, data: Dict[str, Any], retry_count: int = 0) -> AsyncGenerator[str, None]:
        """发送流式请求并处理重试逻辑
        
        Args:
            url: API端点URL
            data: 请求数据
            retry_count: 当前重试次数
            
        Returns:
            流式响应生成器
            
        Raises:
            APIError: API调用失败
        """
        try:
            session = await self.session
            async with session.post(url, json=data) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"流式API调用失败: {response.status} - {error_text}")
                    raise APIError(f"DeepSeek流式API调用失败: {response.status} - {error_text}")
                
                async for line in response.content:
                    if line:
                        try:
                            line_text = line.decode("utf-8").replace("data: ", "")
                            logger.debug(f"流式响应行: {line_text}")
                            event = json.loads(line_text)
                            if event["choices"][0]["delta"].get("content"):
                                content = event["choices"][0]["delta"]["content"]
                                logger.debug(f"流式内容片段: {content}")
                                yield content
                        except Exception as e:
                            logger.warning(f"解析流式响应失败: {str(e)}")
                            continue
                            
        except (aiohttp.ClientError, socket.gaierror, asyncio.TimeoutError) as e:
            if retry_count < MAX_RETRIES:
                logger.warning(f"流式API请求失败，将在{RETRY_DELAY}秒后重试 ({retry_count + 1}/{MAX_RETRIES}): {str(e)}")
                await asyncio.sleep(RETRY_DELAY)
                async for chunk in self._make_stream_request(url, data, retry_count + 1):
                    yield chunk
            else:
                logger.error(f"流式API请求在{MAX_RETRIES}次重试后仍然失败: {str(e)}")
                raise APIError(f"DeepSeek流式API调用失败: {str(e)}")
        except Exception as e:
            logger.error(f"流式API请求出现未预期的错误: {str(e)}", exc_info=True)
            raise APIError(f"DeepSeek流式API调用失败: {str(e)}")
    
    async def stream_chat(self,
                         messages: List[Dict[str, str]],
                         system_info: Dict[str, Any]
                         ) -> AsyncGenerator[str, None]:
        """流式聊天
        
        Args:
            messages: 消息列表
            system_info: 系统信息
            
        Returns:
            聊天响应生成器
            
        Raises:
            APIError: API调用错误
        """
        try:
            # 添加系统信息
            all_messages = [
                {
                    "role": "system",
                    "content": """你是一个命令行助手。你的任务是将用户的自然语言输入转换为具体的命令。
你必须以JSON格式返回响应，格式如下：
{
    "command": "具体的命令",
    "explanation": "命令的解释",
    "warnings": ["可能的风险提示"]
}

系统信息：""" + json.dumps(system_info)
                }
            ]
            all_messages.extend(messages)
            logger.debug(f"流式聊天消息: {json.dumps(all_messages, ensure_ascii=False)}")
            
            # 调用流式API
            data = {
                "model": self.model,
                "messages": all_messages,
                "temperature": self.temperature,
                "stream": True
            }
            logger.debug(f"流式API请求数据: {json.dumps(data, ensure_ascii=False)}")
            
            # 发送流式请求
            async for chunk in self._make_stream_request(self.API_URL, data):
                yield chunk
                        
        except Exception as e:
            logger.error(f"流式聊天出错: {str(e)}", exc_info=True)
            raise APIError(f"DeepSeek流式API调用失败: {str(e)}")


class AIInterface:
    """AI接口类"""
    
    PROVIDERS = {
        "openai": OpenAIProvider,
        "deepseek": DeepSeekProvider
    }
    
    def __init__(self, provider: str = "deepseek", model: Optional[str] = None, api_key: Optional[str] = None):
        """初始化AI接口
        
        Args:
            provider: AI提供商名称
            model: 模型名称
            api_key: API密钥
        """
        if provider not in self.PROVIDERS:
            raise ValueError(f"不支持的AI提供商: {provider}")
            
        self.provider_name = provider
        self.provider_class = self.PROVIDERS[provider]
        
        # 如果未指定模型，使用提供商的默认模型
        if not model:
            model = self.provider_class.DEFAULT_MODEL
            
        if not api_key:
            raise ValueError(f"未提供API密钥")
            
        # 创建提供商实例
        self.provider = self.provider_class(
            api_key=api_key,
            model=model
        )
        
        # 初始化历史记录
        self.history: List[Dict[str, str]] = []
    
    async def generate_command(self, 
                             user_input: str,
                             system_info: Dict[str, Any],
                             history: Optional[List[Dict[str, str]]] = None
                             ) -> Dict[str, Any]:
        """生成命令
        
        Args:
            user_input: 用户输入
            system_info: 系统信息
            history: 历史记录
            
        Returns:
            包含命令和解释的字典
            
        Raises:
            AIError: AI服务错误
            APIError: API调用错误
        """
        try:
            return await self.provider.generate_command(
                user_input=user_input,
                system_info=system_info,
                history=history or self.history
            )
        except Exception as e:
            logger.error(f"生成命令失败: {str(e)}", exc_info=True)
            raise
    
    async def chat(self, message: str) -> str:
        """处理聊天消息
        
        Args:
            message: 用户消息
            
        Returns:
            AI响应
            
        Raises:
            AIError: AI服务错误
            APIError: API调用错误
        """
        try:
            # 生成命令
            command_data = await self.generate_command(
                user_input=message,
                system_info={},  # 这里可以添加系统信息
                history=self.history
            )
            
            # 保存对话历史
            self.history.append({
                "user": message,
                "assistant": command_data.get("command", "")
            })
            
            return command_data.get("command", "")
            
        except Exception as e:
            logger.error(f"AI处理失败: {str(e)}", exc_info=True)
            raise
    
    def get_history(self) -> List[Dict[str, str]]:
        """获取对话历史
        
        Returns:
            对话历史列表
        """
        return self.history

