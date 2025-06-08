# AI终端助手开发者指南

本文档为希望为AI终端助手（ATA）项目做出贡献或扩展其功能的开发者提供指导。

## 目录

1. [项目结构](#项目结构)
2. [开发环境设置](#开发环境设置)
3. [核心模块](#核心模块)
4. [扩展功能](#扩展功能)
5. [测试](#测试)
6. [代码风格](#代码风格)
7. [文档](#文档)
8. [发布流程](#发布流程)
9. [贡献指南](#贡献指南)

## 项目结构

AI终端助手的项目结构如下：

```
ai-terminal-assistant/
├── ata/                    # 主源代码目录
│   ├── __init__.py         # 包初始化文件
│   ├── ai_interface.py     # AI模型接口
│   ├── cli.py              # 命令行界面
│   ├── command_executor.py # 命令执行模块
│   └── config_manager.py   # 配置管理模块
├── docs/                   # 文档目录
│   ├── installation.md     # 安装指南
│   └── user_manual.md      # 用户手册
├── examples/               # 示例目录
│   ├── __init__.py
│   ├── mock_test.py        # 模拟测试示例
│   └── simple_demo.py      # 简单演示示例
├── tests/                  # 测试目录
│   ├── __init__.py
│   ├── test_ai_interface.py    # AI接口测试
│   └── test_command_executor.py # 命令执行测试
├── .gitignore              # Git忽略文件
├── LICENSE                 # 许可证文件
├── README.md               # 项目说明文件
└── setup.py                # 安装脚本
```

## 开发环境设置

### 前提条件

- Python 3.8或更高版本
- Git
- 编辑器或IDE（推荐VS Code或PyCharm）
- OpenAI API密钥（用于测试）
- DeepSeek API密钥（可选，用于测试DeepSeek模型）

### 设置步骤

1. **克隆仓库**

   ```bash
   git clone https://github.com/username/ai-terminal-assistant.git
   cd ai-terminal-assistant
   ```

2. **创建虚拟环境**

   ```bash
   # 创建虚拟环境
   python -m venv venv
   
   # 激活虚拟环境
   # Linux/macOS
   source venv/bin/activate
   # Windows
   venv\Scripts\activate
   ```

3. **安装开发依赖**

   ```bash
   # 安装开发模式
   pip install -e ".[dev]"
   ```

4. **设置API密钥**

   ```bash
   # OpenAI API密钥
   # Linux/macOS
   export OPENAI_API_KEY="your-openai-api-key"
   # Windows
   set OPENAI_API_KEY=your-openai-api-key
   
   # DeepSeek API密钥（可选）
   # Linux/macOS
   export DEEPSEEK_API_KEY="your-deepseek-api-key"
   # Windows
   set DEEPSEEK_API_KEY=your-deepseek-api-key
   ```

5. **运行测试**

   ```bash
   # 运行所有测试
   python -m unittest discover tests
   
   # 运行特定测试
   python -m unittest tests/test_ai_interface.py
   
   # 测试特定模型提供商
   python examples/mock_test.py --provider openai
   python examples/mock_test.py --provider deepseek
   ```

## 核心模块

### AI模型接口 (`ai_interface.py`)

AI模型接口负责与AI API通信，将用户的自然语言请求转换为命令。主要功能包括：

- 构建API请求
- 解析API响应
- 处理错误和超时
- 提取命令和解释

关键类和方法：

- `BaseModelInterface`: 基础接口类
  - `__init__(self, api_key=None, model=None, timeout=30)`: 初始化接口
  - `generate_command(self, user_input, system_info, history=None)`: 生成命令（抽象方法）
  - `_build_prompt(self, user_input, system_info)`: 构建提示
  - `_parse_response(self, response_text)`: 解析响应

- `OpenAIModelInterface`: OpenAI模型接口类
  - `__init__(self, api_key=None, model="gpt-4o", timeout=30)`: 初始化OpenAI接口
  - `generate_command(self, user_input, system_info, history=None)`: 生成命令

- `DeepSeekModelInterface`: DeepSeek模型接口类
  - `__init__(self, api_key=None, model="deepseek-v3-0324", timeout=30)`: 初始化DeepSeek接口
  - `generate_command(self, user_input, system_info, history=None)`: 生成命令

- `ModelFactory`: 模型工厂类
  - `create_model(provider="openai", api_key=None, model=None, timeout=30)`: 创建模型接口实例

扩展此模块时，可以：
- 添加对其他AI提供商的支持
- 实现本地模型集成
- 优化提示模板
- 添加更多上下文处理
- 实现模型性能监控和自动切换

### 命令执行模块 (`command_executor.py`)

命令执行模块负责安全地执行生成的命令并处理结果。主要功能包括：

- 检测命令是否危险
- 执行命令
- 处理超时和错误
- 格式化执行结果

关键类和方法：

- `CommandExecutor`: 主执行器类
  - `__init__(self, shell=None, timeout=60)`: 初始化执行器
  - `execute(self, command, timeout=None)`: 执行命令
  - `is_dangerous(self, command)`: 检测命令是否危险
  - `_detect_shell(self)`: 检测当前shell

扩展此模块时，可以：
- 添加更多危险命令模式
- 实现沙箱执行环境
- 添加命令历史记录
- 优化不同操作系统的兼容性

### 命令行界面 (`cli.py`)

命令行界面负责处理用户输入和显示结果。主要功能包括：

- 解析命令行参数
- 处理用户输入
- 显示命令和解释
- 获取用户确认
- 显示执行结果
- 管理多模型提供商和自动回退

关键类和方法：

- `CLI`: 主界面类
  - `__init__(self, ai_interface=None, command_executor=None, config_manager=None, auto_fallback=False, fallback_provider=None)`: 初始化界面
  - `process_request(self, user_input)`: 处理用户请求
  - `get_confirmation(self, command_data)`: 获取用户确认
  - `display_result(self, result)`: 显示执行结果
  - `run_interactive(self)`: 运行交互模式
  - `_try_fallback(self, user_input, system_info)`: 尝试使用回退提供商

扩展此模块时，可以：
- 添加更多命令行选项
- 实现彩色输出
- 添加进度指示器
- 实现自动补全
- 优化多模型提供商的切换逻辑

### 配置管理模块 (`config_manager.py`)

配置管理模块负责加载和保存用户配置。主要功能包括：

- 加载配置文件
- 合并环境变量和默认值
- 验证配置
- 保存配置
- 管理多模型提供商配置

关键类和方法：

- `ConfigManager`: 主配置类
  - `__init__(self, config_file=None)`: 初始化配置管理器
  - `load(self)`: 加载配置
  - `save(self)`: 保存配置
  - `get(self, key, default=None)`: 获取配置值
  - `set(self, key, value)`: 设置配置值

扩展此模块时，可以：
- 添加配置迁移
- 实现配置验证
- 添加配置UI
- 支持多配置文件
- 优化多模型提供商的配置管理

## 扩展功能

### 添加新的AI提供商

AI终端助手现在支持两种AI提供商：OpenAI和DeepSeek。要添加对新的AI提供商的支持，可以按照以下步骤操作：

1. 在`ai_interface.py`中创建新的提供商类，继承`BaseModelInterface`：

   ```python
   class AnthropicModelInterface(BaseModelInterface):
       """Anthropic模型接口类"""
       
       def __init__(self, api_key=None, model="claude-3-opus", timeout=30):
           """
           初始化Anthropic模型接口
           
           参数:
               api_key (str, 可选): Anthropic API密钥。如果未提供，将尝试从环境变量ANTHROPIC_API_KEY获取。
               model (str, 可选): 使用的AI模型。默认为"claude-3-opus"。
               timeout (int, 可选): API请求超时时间（秒）。默认为30。
               
           异常:
               ValueError: 如果API密钥未提供或无效。
           """
           # 如果未提供API密钥，尝试从环境变量获取
           if api_key is None:
               import os
               api_key = os.environ.get("ANTHROPIC_API_KEY")
           
           if not api_key:
               raise ValueError("Anthropic API密钥未提供。请设置ANTHROPIC_API_KEY环境变量或在初始化时提供api_key参数。")
           
           super().__init__(api_key, model, timeout)
       
       def generate_command(self, user_input, system_info, history=None):
           """
           生成命令
           
           参数:
               user_input (str): 用户输入的自然语言请求
               system_info (dict): 系统信息，包括操作系统、shell类型等
               history (list, 可选): 历史记录，用于上下文理解
               
           返回:
               dict: 包含以下键的字典:
                   - success (bool): 是否成功生成命令
                   - command (str): 生成的命令，如果失败则为None
                   - explanation (str): 命令的解释，如果失败则为None
                   - warnings (list): 警告列表，如果有的话
                   
           异常:
               APIError: 如果API请求失败
               TimeoutError: 如果API请求超时
           """
           import requests
           import json
           
           prompt = self._build_prompt(user_input, system_info)
           
           try:
               headers = {
                   "Content-Type": "application/json",
                   "X-API-Key": self.api_key
               }
               
               data = {
                   "model": self.model,
                   "messages": [
                       {"role": "system", "content": prompt},
                       {"role": "user", "content": user_input}
                   ],
                   "temperature": 0.2,
                   "max_tokens": 500
               }
               
               response = requests.post(
                   "https://api.anthropic.com/v1/messages",
                   headers=headers,
                   json=data,
                   timeout=self.timeout
               )
               
               if response.status_code != 200:
                   return {
                       "success": False,
                       "command": None,
                       "explanation": None,
                       "warnings": [f"Anthropic API错误: HTTP {response.status_code} - {response.text}"]
                   }
               
               response_json = response.json()
               response_text = response_json["content"][0]["text"]
               return self._parse_response(response_text)
           except requests.Timeout:
               return {
                   "success": False,
                   "command": None,
                   "explanation": None,
                   "warnings": ["Anthropic API请求超时。请稍后重试或检查您的网络连接。"]
               }
           except requests.RequestException as e:
               return {
                   "success": False,
                   "command": None,
                   "explanation": None,
                   "warnings": [f"Anthropic API请求错误: {str(e)}"]
               }
           except Exception as e:
               return {
                   "success": False,
                   "command": None,
                   "explanation": None,
                   "warnings": [f"生成命令时出错: {str(e)}"]
               }
   ```

2. 在`ModelFactory`类中添加对新提供商的支持：

   ```python
   @staticmethod
   def create_model(provider="openai", api_key=None, model=None, timeout=30):
       """
       创建模型接口实例
       
       参数:
           provider (str, 可选): 模型提供商，可选值为"openai"、"deepseek"或"anthropic"。默认为"openai"。
           api_key (str, 可选): API密钥。如果未提供，将尝试从环境变量获取。
           model (str, 可选): 使用的AI模型。如果未提供，将使用默认模型。
           timeout (int, 可选): API请求超时时间（秒）。默认为30。
           
       返回:
           BaseModelInterface: 模型接口实例
           
       异常:
           ValueError: 如果提供商无效或API密钥未提供或无效。
       """
       provider = provider.lower()
       
       if provider == "openai":
           # 如果未提供模型，使用默认模型
           if model is None:
               import os
               model = os.environ.get("ATA_OPENAI_MODEL", "gpt-4o")
           
           return OpenAIModelInterface(api_key=api_key, model=model, timeout=timeout)
       elif provider == "deepseek":
           # 如果未提供模型，使用默认模型
           if model is None:
               import os
               model = os.environ.get("ATA_DEEPSEEK_MODEL", "deepseek-v3-0324")
           
           return DeepSeekModelInterface(api_key=api_key, model=model, timeout=timeout)
       elif provider == "anthropic":
           # 如果未提供模型，使用默认模型
           if model is None:
               import os
               model = os.environ.get("ATA_ANTHROPIC_MODEL", "claude-3-opus")
           
           return AnthropicModelInterface(api_key=api_key, model=model, timeout=timeout)
       else:
           raise ValueError(f"无效的模型提供商: {provider}。支持的提供商有: openai, deepseek, anthropic")
   ```

3. 在`config_manager.py`中添加新提供商的默认配置：

   ```python
   DEFAULT_CONFIG = {
       "ai": {
           "provider": "openai",  # 可选值: openai, deepseek, anthropic
           "fallback_provider": "deepseek",  # 当主要提供商失败时使用的提供商
           "auto_fallback": False,  # 是否自动使用回退提供商
           "timeout": 30,  # API请求超时时间（秒）
           "openai": {
               "api_key": None,  # 将从环境变量OPENAI_API_KEY获取
               "model": "gpt-4o"
           },
           "deepseek": {
               "api_key": None,  # 将从环境变量DEEPSEEK_API_KEY获取
               "model": "deepseek-v3-0324"
           },
           "anthropic": {
               "api_key": None,  # 将从环境变量ANTHROPIC_API_KEY获取
               "model": "claude-3-opus"
           }
       },
       "execution": {
           "shell": None,  # 如果为None，将自动检测
           "timeout": 60,  # 命令执行超时时间（秒）
           "confirm_dangerous": True  # 是否确认危险命令
       },
       "ui": {
           "color": True,  # 是否使用彩色输出
           "verbose": False  # 是否显示详细信息
       }
   }
   ```

4. 在`cli.py`中添加对新提供商的支持：

   ```python
   def _parse_args(self):
       import argparse
       
       parser = argparse.ArgumentParser(description="AI终端助手")
       parser.add_argument("input", nargs="?", help="用户输入")
       parser.add_argument("--version", action="store_true", help="显示版本信息")
       parser.add_argument("--provider", choices=["openai", "deepseek", "anthropic"], help="指定AI提供商")
       parser.add_argument("--model", help="指定AI模型")
       parser.add_argument("--fallback", action="store_true", help="启用自动回退机制")
       parser.add_argument("--fallback-provider", choices=["openai", "deepseek", "anthropic"], help="指定回退AI提供商")
       parser.add_argument("--timeout", type=int, help="设置超时时间（秒）")
       parser.add_argument("--no-color", action="store_true", help="禁用彩色输出")
       parser.add_argument("--verbose", action="store_true", help="启用详细输出")
       
       return parser.parse_args()
   ```

### 实现模型性能监控和自动切换

要实现模型性能监控和自动切换功能，可以创建一个新的`ModelMonitor`类：

```python
# ata/model_monitor.py
import time
import json
import os
from typing import Dict, List, Optional, Any

class ModelMonitor:
    """模型性能监控器"""
    
    def __init__(self, history_file=None):
        """
        初始化模型性能监控器
        
        参数:
            history_file (str, 可选): 历史记录文件路径。如果为None，将使用默认路径~/.ata/model_history.json。
        """
        if history_file is None:
            home_dir = os.path.expanduser("~")
            ata_dir = os.path.join(home_dir, ".ata")
            os.makedirs(ata_dir, exist_ok=True)
            history_file = os.path.join(ata_dir, "model_history.json")
        
        self.history_file = history_file
        self.history = self._load_history()
    
    def _load_history(self) -> Dict[str, Any]:
        """
        加载历史记录
        
        返回:
            dict: 加载的历史记录
        """
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r") as f:
                    return json.load(f)
            except Exception:
                pass
        
        return {
            "providers": {},
            "requests": []
        }
    
    def _save_history(self) -> bool:
        """
        保存历史记录
        
        返回:
            bool: 是否成功保存
        """
        try:
            with open(self.history_file, "w") as f:
                json.dump(self.history, f, indent=2)
            return True
        except Exception:
            return False
    
    def record_request(self, provider: str, model: str, user_input: str, success: bool, duration: float) -> None:
        """
        记录请求
        
        参数:
            provider (str): 提供商名称
            model (str): 模型名称
            user_input (str): 用户输入
            success (bool): 是否成功
            duration (float): 持续时间（秒）
        """
        # 更新提供商统计
        if provider not in self.history["providers"]:
            self.history["providers"][provider] = {
                "total_requests": 0,
                "successful_requests": 0,
                "total_duration": 0.0,
                "models": {}
            }
        
        provider_stats = self.history["providers"][provider]
        provider_stats["total_requests"] += 1
        if success:
            provider_stats["successful_requests"] += 1
        provider_stats["total_duration"] += duration
        
        # 更新模型统计
        if model not in provider_stats["models"]:
            provider_stats["models"][model] = {
                "total_requests": 0,
                "successful_requests": 0,
                "total_duration": 0.0
            }
        
        model_stats = provider_stats["models"][model]
        model_stats["total_requests"] += 1
        if success:
            model_stats["successful_requests"] += 1
        model_stats["total_duration"] += duration
        
        # 添加请求记录
        self.history["requests"].append({
            "timestamp": time.time(),
            "provider": provider,
            "model": model,
            "success": success,
            "duration": duration
        })
        
        # 限制请求记录数量
        if len(self.history["requests"]) > 1000:
            self.history["requests"] = self.history["requests"][-1000:]
        
        # 保存历史记录
        self._save_history()
    
    def get_provider_stats(self, provider: str) -> Optional[Dict[str, Any]]:
        """
        获取提供商统计
        
        参数:
            provider (str): 提供商名称
            
        返回:
            dict: 提供商统计，如果不存在则为None
        """
        return self.history["providers"].get(provider)
    
    def get_model_stats(self, provider: str, model: str) -> Optional[Dict[str, Any]]:
        """
        获取模型统计
        
        参数:
            provider (str): 提供商名称
            model (str): 模型名称
            
        返回:
            dict: 模型统计，如果不存在则为None
        """
        provider_stats = self.get_provider_stats(provider)
        if provider_stats:
            return provider_stats["models"].get(model)
        return None
    
    def get_success_rate(self, provider: str, model: Optional[str] = None) -> float:
        """
        获取成功率
        
        参数:
            provider (str): 提供商名称
            model (str, 可选): 模型名称。如果为None，将返回提供商的整体成功率。
            
        返回:
            float: 成功率（0.0-1.0）
        """
        if model:
            stats = self.get_model_stats(provider, model)
        else:
            stats = self.get_provider_stats(provider)
        
        if stats and stats["total_requests"] > 0:
            return stats["successful_requests"] / stats["total_requests"]
        return 0.0
    
    def get_average_duration(self, provider: str, model: Optional[str] = None) -> float:
        """
        获取平均持续时间
        
        参数:
            provider (str): 提供商名称
            model (str, 可选): 模型名称。如果为None，将返回提供商的整体平均持续时间。
            
        返回:
            float: 平均持续时间（秒）
        """
        if model:
            stats = self.get_model_stats(provider, model)
        else:
            stats = self.get_provider_stats(provider)
        
        if stats and stats["total_requests"] > 0:
            return stats["total_duration"] / stats["total_requests"]
        return 0.0
    
    def get_best_provider(self, candidates: List[str] = None) -> str:
        """
        获取最佳提供商
        
        参数:
            candidates (list, 可选): 候选提供商列表。如果为None，将使用所有提供商。
            
        返回:
            str: 最佳提供商名称
        """
        if candidates is None:
            candidates = list(self.history["providers"].keys())
        
        if not candidates:
            return "openai"  # 默认提供商
        
        # 计算每个提供商的得分
        scores = {}
        for provider in candidates:
            stats = self.get_provider_stats(provider)
            if stats and stats["total_requests"] > 0:
                success_rate = self.get_success_rate(provider)
                avg_duration = self.get_average_duration(provider)
                
                # 得分 = 成功率 - 归一化的持续时间
                # 持续时间越短越好，但成功率更重要
                score = success_rate - (avg_duration / 10.0)
                scores[provider] = score
            else:
                scores[provider] = 0.0
        
        # 返回得分最高的提供商
        if scores:
            return max(scores.items(), key=lambda x: x[1])[0]
        
        return candidates[0]  # 如果没有统计数据，返回第一个候选提供商
```

然后，在`cli.py`中使用`ModelMonitor`：

```python
from ata.model_monitor import ModelMonitor

class CLI:
    """命令行界面类"""
    
    def __init__(self, ai_interface=None, command_executor=None, config_manager=None, auto_fallback=False, fallback_provider=None):
        # ...
        self.model_monitor = ModelMonitor()
    
    def process_request(self, user_input):
        """处理用户请求"""
        # 获取系统信息
        system_info = get_system_info()
        
        # 记录开始时间
        start_time = time.time()
        
        # 生成命令
        try:
            command_data = self.ai_interface.generate_command(user_input, system_info)
            success = command_data["success"]
        except Exception:
            command_data = {
                "success": False,
                "command": None,
                "explanation": None,
                "warnings": ["生成命令时出错。请稍后重试。"]
            }
            success = False
        
        # 记录持续时间
        duration = time.time() - start_time
        
        # 记录请求
        provider = self.config.get("ai.provider", "openai")
        model = self.ai_interface.model
        self.model_monitor.record_request(provider, model, user_input, success, duration)
        
        # 如果失败且启用了自动回退，尝试使用回退提供商
        if not success and self.auto_fallback:
            return self._try_fallback(user_input, system_info)
        
        return command_data
    
    def _try_fallback(self, user_input, system_info):
        """尝试使用回退提供商"""
        # 获取回退提供商
        fallback_provider = self.fallback_provider or self.config.get("ai.fallback_provider", "deepseek")
        
        # 如果回退提供商与当前提供商相同，尝试使用其他提供商
        current_provider = self.config.get("ai.provider", "openai")
        if fallback_provider == current_provider:
            # 获取所有可用提供商
            available_providers = ["openai", "deepseek"]
            # 移除当前提供商
            available_providers.remove(current_provider)
            # 如果没有其他提供商，返回失败
            if not available_providers:
                return {
                    "success": False,
                    "command": None,
                    "explanation": None,
                    "warnings": ["所有提供商都失败。请稍后重试。"]
                }
            # 使用模型监控器选择最佳提供商
            fallback_provider = self.model_monitor.get_best_provider(available_providers)
        
        # 创建回退提供商的模型接口
        try:
            fallback_interface = ModelFactory.create_model(
                provider=fallback_provider,
                api_key=None,  # 将从环境变量获取
                model=None,    # 将使用默认模型
                timeout=self.config.get("ai.timeout", 30)
            )
            
            # 记录开始时间
            start_time = time.time()
            
            # 生成命令
            command_data = fallback_interface.generate_command(user_input, system_info)
            
            # 记录持续时间
            duration = time.time() - start_time
            
            # 记录请求
            self.model_monitor.record_request(
                fallback_provider,
                fallback_interface.model,
                user_input,
                command_data["success"],
                duration
            )
            
            return command_data
        except Exception as e:
            return {
                "success": False,
                "command": None,
                "explanation": None,
                "warnings": [f"回退提供商也失败: {str(e)}"]
            }
```

### 添加新的命令行选项

要添加新的命令行选项，可以修改`cli.py`中的`_parse_args`方法：

```python
def _parse_args(self):
    import argparse
    
    parser = argparse.ArgumentParser(description="AI终端助手")
    parser.add_argument("input", nargs="?", help="用户输入")
    parser.add_argument("--version", action="store_true", help="显示版本信息")
    parser.add_argument("--provider", choices=["openai", "deepseek", "anthropic"], help="指定AI提供商")
    parser.add_argument("--model", help="指定AI模型")
    parser.add_argument("--fallback", action="store_true", help="启用自动回退机制")
    parser.add_argument("--fallback-provider", choices=["openai", "deepseek", "anthropic"], help="指定回退AI提供商")
    parser.add_argument("--timeout", type=int, help="设置超时时间（秒）")
    parser.add_argument("--no-color", action="store_true", help="禁用彩色输出")
    parser.add_argument("--verbose", action="store_true", help="启用详细输出")
    parser.add_argument("--stats", action="store_true", help="显示模型性能统计")
    parser.add_argument("--batch", help="批处理模式，指定请求文件路径")
    parser.add_argument("--auto-confirm", action="store_true", help="自动确认执行命令（批处理模式）")
    parser.add_argument("--save-history", action="store_true", help="保存命令历史")
    parser.add_argument("--config", help="指定配置文件路径")
    
    return parser.parse_args()
```

## 测试

### 单元测试

AI终端助手使用Python的`unittest`框架进行测试。测试文件位于`tests`目录中。

运行测试：

```bash
# 运行所有测试
python -m unittest discover tests

# 运行特定测试
python -m unittest tests/test_ai_interface.py

# 运行特定测试方法
python -m unittest tests.test_ai_interface.TestOpenAIModelInterface.test_generate_command
```

### 测试多模型提供商

要测试不同的模型提供商，可以使用`examples/mock_test.py`脚本：

```bash
# 测试OpenAI提供商
python examples/mock_test.py --provider openai

# 测试DeepSeek提供商
python examples/mock_test.py --provider deepseek

# 测试自动回退机制
python examples/mock_test.py --fallback
```

### 编写测试

编写新测试时，请遵循以下准则：

1. 测试文件应以`test_`开头
2. 测试类应继承`unittest.TestCase`
3. 测试方法应以`test_`开头
4. 使用`unittest.mock`模拟外部依赖
5. 每个测试应该独立且可重复

示例：

```python
import unittest
from unittest.mock import patch, MagicMock

from ata.ai_interface import OpenAIModelInterface

class TestOpenAIModelInterface(unittest.TestCase):
    """测试OpenAI模型接口"""
    
    def setUp(self):
        """测试前设置"""
        self.ai_interface = OpenAIModelInterface(api_key="test_key")
    
    def tearDown(self):
        """测试后清理"""
        pass
    
    @patch('openai.chat.completions.create')
    def test_generate_command(self, mock_create):
        """测试生成命令功能"""
        # 设置模拟返回值
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"command": "ls -la", "explanation": "列出文件"}'
        mock_create.return_value = mock_response
        
        # 调用被测方法
        result = self.ai_interface.generate_command("列出文件", {"os": "Linux"})
        
        # 验证结果
        self.assertTrue(result["success"])
        self.assertEqual(result["command"], "ls -la")
        self.assertEqual(result["explanation"], "列出文件")
        
        # 验证模拟调用
        mock_create.assert_called_once()
```

### 测试DeepSeek模型接口

要测试DeepSeek模型接口，可以编写类似的测试：

```python
import unittest
from unittest.mock import patch, MagicMock

from ata.ai_interface import DeepSeekModelInterface

class TestDeepSeekModelInterface(unittest.TestCase):
    """测试DeepSeek模型接口"""
    
    def setUp(self):
        """测试前设置"""
        self.ai_interface = DeepSeekModelInterface(api_key="test_key")
    
    def tearDown(self):
        """测试后清理"""
        pass
    
    @patch('requests.post')
    def test_generate_command(self, mock_post):
        """测试生成命令功能"""
        # 设置模拟返回值
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": '{"command": "ls -la", "explanation": "列出文件"}'
                    }
                }
            ]
        }
        mock_post.return_value = mock_response
        
        # 调用被测方法
        result = self.ai_interface.generate_command("列出文件", {"os": "Linux"})
        
        # 验证结果
        self.assertTrue(result["success"])
        self.assertEqual(result["command"], "ls -la")
        self.assertEqual(result["explanation"], "列出文件")
        
        # 验证模拟调用
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(args[0], "https://api.deepseek.com/v1/chat/completions")
        self.assertEqual(kwargs["headers"]["Authorization"], "Bearer test_key")
```

## 代码风格

AI终端助手项目遵循PEP 8代码风格指南，并使用以下工具确保代码质量：

- **Black**：代码格式化
- **isort**：导入排序
- **flake8**：代码检查
- **mypy**：类型检查

### 代码格式化

在提交代码前，请运行以下命令格式化代码：

```bash
# 格式化代码
black ata tests examples

# 排序导入
isort ata tests examples

# 检查代码
flake8 ata tests examples

# 类型检查
mypy ata
```

### 类型注解

AI终端助手使用Python的类型注解来提高代码可读性和可维护性。请在所有函数和方法中添加类型注解：

```python
def generate_command(self, user_input: str, system_info: Dict[str, str], history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
    """
    生成命令
    
    Args:
        user_input: 用户输入
        system_info: 系统信息
        history: 历史记录
        
    Returns:
        包含命令、解释和警告的字典
    """
    # ...
```

## 文档

AI终端助手使用Markdown格式的文档，位于`docs`目录中。主要文档包括：

- `README.md`：项目概述
- `installation.md`：安装指南
- `user_manual.md`：用户手册
- `developer_guide.md`：开发者指南
- `api_reference.md`：API参考

### 文档风格

编写文档时，请遵循以下准则：

1. 使用清晰、简洁的语言
2. 提供具体的示例
3. 使用标题和列表组织内容
4. 包含命令行示例和代码片段
5. 解释所有参数和选项
6. 提供故障排除信息

### 生成API文档

可以使用`pdoc`生成API文档：

```bash
# 安装pdoc
pip install pdoc

# 生成HTML文档
pdoc --html --output-dir docs/api ata

# 生成Markdown文档
pdoc --pdf --output-dir docs/api ata
```

## 发布流程

AI终端助手使用语义化版本控制（Semantic Versioning）。版本号格式为：`MAJOR.MINOR.PATCH`。

### 版本控制

- **MAJOR**：不兼容的API变更
- **MINOR**：向后兼容的功能新增
- **PATCH**：向后兼容的问题修复

### 发布步骤

1. **更新版本号**

   在`ata/__init__.py`中更新版本号：

   ```python
   __version__ = "0.2.0"
   ```

2. **更新变更日志**

   在`CHANGELOG.md`中添加新版本的变更记录：

   ```markdown
   ## [0.2.0] - 2025-06-10

   ### 新增
   - 添加对DeepSeek模型的支持
   - 添加模型自动回退机制
   - 添加模型性能监控
   - 添加命令历史功能
   - 添加彩色输出

   ### 修复
   - 修复Windows上的路径问题
   - 修复超时处理

   ### 变更
   - 改进错误消息
   - 优化提示模板
   ```

3. **创建发布分支**

   ```bash
   git checkout -b release/0.2.0
   git add ata/__init__.py CHANGELOG.md
   git commit -m "准备发布 0.2.0"
   git push origin release/0.2.0
   ```

4. **创建Pull Request**

   在GitHub上创建从`release/0.2.0`到`main`的Pull Request。

5. **合并Pull Request**

   在代码审查和测试通过后，合并Pull Request。

6. **创建标签**

   ```bash
   git checkout main
   git pull
   git tag -a v0.2.0 -m "发布 0.2.0"
   git push origin v0.2.0
   ```

7. **构建和发布**

   ```bash
   # 清理构建目录
   rm -rf build/ dist/ *.egg-info/

   # 构建包
   python setup.py sdist bdist_wheel

   # 发布到PyPI
   twine upload dist/*
   ```

## 贡献指南

我们欢迎所有形式的贡献，包括但不限于：

- 代码贡献
- 文档改进
- 错误报告
- 功能请求
- 代码审查

### 贡献流程

1. **Fork仓库**

   在GitHub上fork仓库到你的账户。

2. **克隆仓库**

   ```bash
   git clone https://github.com/your-username/ai-terminal-assistant.git
   cd ai-terminal-assistant
   ```

3. **创建分支**

   ```bash
   git checkout -b feature/amazing-feature
   ```

4. **进行更改**

   进行你的更改，确保遵循代码风格指南。

5. **运行测试**

   ```bash
   python -m unittest discover tests
   ```

6. **提交更改**

   ```bash
   git add .
   git commit -m "添加一个很棒的功能"
   ```

7. **推送到分支**

   ```bash
   git push origin feature/amazing-feature
   ```

8. **创建Pull Request**

   在GitHub上创建从你的分支到原仓库`main`分支的Pull Request。

### Pull Request指南

- 每个Pull Request应该只包含一个功能或修复
- 提供清晰的描述，解释你的更改
- 包含相关测试
- 确保所有测试通过
- 更新相关文档

### 行为准则

请尊重所有贡献者和用户，保持友好和建设性的交流。

---

感谢你对AI终端助手项目的贡献！如果你有任何问题，请随时联系我们。

