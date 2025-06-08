# AI终端助手 API参考

本文档提供了AI终端助手（ATA）的API参考，适用于希望将ATA集成到其他项目中的开发者。

## 目录

1. [模块概述](#模块概述)
2. [AI模型接口](#ai模型接口)
   - [基础模型接口](#基础模型接口)
   - [OpenAI模型接口](#openai模型接口)
   - [DeepSeek模型接口](#deepseek模型接口)
   - [模型工厂](#模型工厂)
3. [命令执行模块](#命令执行模块)
4. [配置管理模块](#配置管理模块)
5. [命令行界面](#命令行界面)
6. [工具函数](#工具函数)
7. [异常类](#异常类)
8. [类型定义](#类型定义)
9. [示例](#示例)

## 模块概述

AI终端助手由以下主要模块组成：

- `ata.ai_interface`: AI模型接口，负责与AI API通信
- `ata.command_executor`: 命令执行模块，负责安全地执行命令
- `ata.config_manager`: 配置管理模块，负责加载和保存配置
- `ata.cli`: 命令行界面，负责处理用户输入和显示结果

## AI模型接口

### 基础模型接口

#### `ata.ai_interface.BaseModelInterface`

AI模型接口基类，定义了所有模型接口的通用方法和属性。

```python
class BaseModelInterface:
    """AI模型接口基类"""
    
    def __init__(self, api_key=None, model=None, timeout=30):
        """
        初始化基础模型接口
        
        参数:
            api_key (str, 可选): API密钥
            model (str, 可选): 使用的AI模型
            timeout (int, 可选): API请求超时时间（秒）。默认为30。
        """
        self.api_key = api_key
        self.model = model
        self.timeout = timeout
    
    def generate_command(self, user_input, system_info, history=None):
        """
        生成命令（抽象方法，需要子类实现）
        
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
            NotImplementedError: 子类必须实现此方法
        """
        raise NotImplementedError("子类必须实现generate_command方法")
    
    def _build_prompt(self, user_input, system_info):
        """
        构建提示
        
        参数:
            user_input (str): 用户输入的自然语言请求
            system_info (dict): 系统信息，包括操作系统、shell类型等
            
        返回:
            str: 构建的提示
        """
        # 构建基本提示模板
        prompt = f"""你是一个命令行专家，请根据用户的请求生成适合{system_info['os']}系统的命令。
用户的工作目录是：{system_info['working_directory']}
用户的shell是：{system_info['shell']}

请按照以下JSON格式返回结果：
{{
  "command": "生成的命令",
  "explanation": "命令的详细解释，包括每个参数的作用",
  "warnings": ["可能的风险或注意事项，如果没有则为空数组"]
}}

用户请求：{user_input}
"""
        return prompt
    
    def _parse_response(self, response_text):
        """
        解析API响应文本
        
        参数:
            response_text (str): API响应文本
            
        返回:
            dict: 解析后的结果，包含命令、解释和警告
        """
        # 尝试解析JSON响应
        try:
            # 尝试提取JSON部分
            import re
            import json
            
            # 查找JSON对象
            json_match = re.search(r'({[\s\S]*})', response_text)
            if json_match:
                json_str = json_match.group(1)
                data = json.loads(json_str)
                
                return {
                    "success": True,
                    "command": data.get("command"),
                    "explanation": data.get("explanation"),
                    "warnings": data.get("warnings", [])
                }
        except Exception:
            pass
        
        # 如果JSON解析失败，尝试从文本中提取命令
        try:
            lines = response_text.split('\n')
            command = None
            explanation = []
            warnings = []
            
            for line in lines:
                line = line.strip()
                if not command and (line.startswith('$') or line.startswith('#')):
                    command = line[1:].strip()
                elif line.lower().startswith('warning') or line.lower().startswith('注意') or line.lower().startswith('警告'):
                    warnings.append(line)
                elif command and not line.startswith('$') and not line.startswith('#'):
                    explanation.append(line)
            
            if command:
                return {
                    "success": True,
                    "command": command,
                    "explanation": '\n'.join(explanation).strip(),
                    "warnings": warnings
                }
        except Exception:
            pass
        
        # 如果所有解析方法都失败，返回错误
        return {
            "success": False,
            "command": None,
            "explanation": None,
            "warnings": ["无法解析AI响应。请尝试重新表述您的请求。"]
        }
```

### OpenAI模型接口

#### `ata.ai_interface.OpenAIModelInterface`

OpenAI模型接口类，负责与OpenAI API通信。

```python
class OpenAIModelInterface(BaseModelInterface):
    """OpenAI模型接口类"""
    
    def __init__(self, api_key=None, model="gpt-4o", timeout=30):
        """
        初始化OpenAI模型接口
        
        参数:
            api_key (str, 可选): OpenAI API密钥。如果未提供，将尝试从环境变量OPENAI_API_KEY获取。
            model (str, 可选): 使用的AI模型。默认为"gpt-4o"。
            timeout (int, 可选): API请求超时时间（秒）。默认为30。
            
        异常:
            ValueError: 如果API密钥未提供或无效。
        """
        # 如果未提供API密钥，尝试从环境变量获取
        if api_key is None:
            import os
            api_key = os.environ.get("OPENAI_API_KEY")
        
        if not api_key:
            raise ValueError("OpenAI API密钥未提供。请设置OPENAI_API_KEY环境变量或在初始化时提供api_key参数。")
        
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
        import openai
        from openai import OpenAI
        
        prompt = self._build_prompt(user_input, system_info)
        
        try:
            client = OpenAI(api_key=self.api_key)
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.2,
                max_tokens=500,
                timeout=self.timeout
            )
            
            response_text = response.choices[0].message.content
            return self._parse_response(response_text)
        except openai.APITimeoutError:
            return {
                "success": False,
                "command": None,
                "explanation": None,
                "warnings": ["OpenAI API请求超时。请稍后重试或检查您的网络连接。"]
            }
        except openai.APIError as e:
            return {
                "success": False,
                "command": None,
                "explanation": None,
                "warnings": [f"OpenAI API错误: {str(e)}"]
            }
        except Exception as e:
            return {
                "success": False,
                "command": None,
                "explanation": None,
                "warnings": [f"生成命令时出错: {str(e)}"]
            }
```

### DeepSeek模型接口

#### `ata.ai_interface.DeepSeekModelInterface`

DeepSeek模型接口类，负责与DeepSeek API通信。

```python
class DeepSeekModelInterface(BaseModelInterface):
    """DeepSeek模型接口类"""
    
    def __init__(self, api_key=None, model="deepseek-v3-0324", timeout=30):
        """
        初始化DeepSeek模型接口
        
        参数:
            api_key (str, 可选): DeepSeek API密钥。如果未提供，将尝试从环境变量DEEPSEEK_API_KEY获取。
            model (str, 可选): 使用的AI模型。默认为"deepseek-v3-0324"。
            timeout (int, 可选): API请求超时时间（秒）。默认为30。
            
        异常:
            ValueError: 如果API密钥未提供或无效。
        """
        # 如果未提供API密钥，尝试从环境变量获取
        if api_key is None:
            import os
            api_key = os.environ.get("DEEPSEEK_API_KEY")
        
        if not api_key:
            raise ValueError("DeepSeek API密钥未提供。请设置DEEPSEEK_API_KEY环境变量或在初始化时提供api_key参数。")
        
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
                "Authorization": f"Bearer {self.api_key}"
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
                "https://api.deepseek.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=self.timeout
            )
            
            if response.status_code != 200:
                return {
                    "success": False,
                    "command": None,
                    "explanation": None,
                    "warnings": [f"DeepSeek API错误: HTTP {response.status_code} - {response.text}"]
                }
            
            response_json = response.json()
            response_text = response_json["choices"][0]["message"]["content"]
            return self._parse_response(response_text)
        except requests.Timeout:
            return {
                "success": False,
                "command": None,
                "explanation": None,
                "warnings": ["DeepSeek API请求超时。请稍后重试或检查您的网络连接。"]
            }
        except requests.RequestException as e:
            return {
                "success": False,
                "command": None,
                "explanation": None,
                "warnings": [f"DeepSeek API请求错误: {str(e)}"]
            }
        except Exception as e:
            return {
                "success": False,
                "command": None,
                "explanation": None,
                "warnings": [f"生成命令时出错: {str(e)}"]
            }
```

### 模型工厂

#### `ata.ai_interface.ModelFactory`

模型工厂类，负责创建适当的模型接口实例。

```python
class ModelFactory:
    """模型工厂类，负责创建适当的模型接口实例"""
    
    @staticmethod
    def create_model(provider="openai", api_key=None, model=None, timeout=30):
        """
        创建模型接口实例
        
        参数:
            provider (str, 可选): 模型提供商，可选值为"openai"或"deepseek"。默认为"openai"。
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
        else:
            raise ValueError(f"无效的模型提供商: {provider}。支持的提供商有: openai, deepseek")
```

### `ata.ai_interface.APIError`

API错误异常类，表示API请求失败。

```python
class APIError(Exception):
    """API错误异常"""
    pass
```

## 命令执行模块

### `ata.command_executor.CommandExecutor`

命令执行器类，负责安全地执行命令并处理结果。

#### 构造函数

```python
def __init__(self, shell=None, timeout=60):
    """
    初始化命令执行器
    
    参数:
        shell (str, 可选): 使用的shell类型。如果为None，将自动检测。
        timeout (int, 可选): 命令执行超时时间（秒）。默认为60。
    """
```

#### 方法

##### `execute`

```python
def execute(self, command, timeout=None):
    """
    执行命令
    
    参数:
        command (str): 要执行的命令
        timeout (int, 可选): 超时时间（秒）。如果为None，将使用默认超时时间。
        
    返回:
        dict: 包含以下键的字典:
            - success (bool): 是否成功执行
            - exit_code (int): 退出代码，如果超时则为None
            - stdout (str): 标准输出
            - stderr (str): 标准错误
            - duration (float): 执行时间（秒）
    """
```

##### `is_dangerous`

```python
def is_dangerous(self, command):
    """
    检测命令是否危险
    
    参数:
        command (str): 要检测的命令
        
    返回:
        tuple: (is_dangerous, warnings)
            - is_dangerous (bool): 命令是否危险
            - warnings (list): 警告列表，如果有的话
    """
```

##### `_detect_shell`

```python
def _detect_shell(self):
    """
    检测当前shell类型
    
    返回:
        str: shell类型，如"bash"、"zsh"、"powershell"等
    """
```

## 配置管理模块

### `ata.config_manager.ConfigManager`

配置管理器类，负责加载和保存配置。

#### 构造函数

```python
def __init__(self, config_file=None):
    """
    初始化配置管理器
    
    参数:
        config_file (str, 可选): 配置文件路径。如果为None，将使用默认路径~/.ata/config.yaml。
    """
```

#### 方法

##### `load`

```python
def load(self):
    """
    加载配置
    
    返回:
        dict: 加载的配置
    """
```

##### `save`

```python
def save(self):
    """
    保存配置
    
    返回:
        bool: 是否成功保存
    """
```

##### `get`

```python
def get(self, key, default=None):
    """
    获取配置值
    
    参数:
        key (str): 配置键，支持点号分隔的路径，如"api.model"
        default (any, 可选): 如果键不存在，返回的默认值
        
    返回:
        any: 配置值，如果键不存在则返回默认值
    """
```

##### `set`

```python
def set(self, key, value):
    """
    设置配置值
    
    参数:
        key (str): 配置键，支持点号分隔的路径，如"api.model"
        value (any): 配置值
        
    返回:
        bool: 是否成功设置
    """
```

## 命令行界面

### `ata.cli.CLI`

命令行界面类，负责处理用户输入和显示结果。

#### 构造函数

```python
def __init__(self, ai_interface=None, command_executor=None, config_manager=None, auto_fallback=False, fallback_provider=None):
    """
    初始化命令行界面
    
    参数:
        ai_interface (BaseModelInterface, 可选): AI模型接口实例。如果为None，将创建新实例。
        command_executor (CommandExecutor, 可选): 命令执行器实例。如果为None，将创建新实例。
        config_manager (ConfigManager, 可选): 配置管理器实例。如果为None，将创建新实例。
        auto_fallback (bool, 可选): 是否启用自动回退机制。默认为False。
        fallback_provider (str, 可选): 回退AI提供商。默认为None，将使用配置中的值或"deepseek"。
    """
```

#### 方法

##### `process_request`

```python
def process_request(self, user_input):
    """
    处理用户请求
    
    参数:
        user_input (str): 用户输入的自然语言请求
        
    返回:
        dict: 执行结果，如果用户取消则为None
    """
```

##### `get_confirmation`

```python
def get_confirmation(self, command_data):
    """
    获取用户确认
    
    参数:
        command_data (dict): 命令数据，包含命令、解释和警告
        
    返回:
        str: 用户选择，可能的值为"y"（执行）、"n"（取消）或"e"（编辑）
    """
```

##### `display_result`

```python
def display_result(self, result):
    """
    显示执行结果
    
    参数:
        result (dict): 执行结果
    """
```

##### `run_interactive`

```python
def run_interactive(self):
    """
    运行交互模式
    
    返回:
        int: 退出代码
    """
```

##### `run`

```python
def run(self):
    """
    运行CLI
    
    返回:
        int: 退出代码
    """
```

## 工具函数

### `ata.utils.format_duration`

```python
def format_duration(seconds):
    """
    格式化持续时间
    
    参数:
        seconds (float): 秒数
        
    返回:
        str: 格式化的持续时间，如"1.5秒"、"2分钟30秒"
    """
```

### `ata.utils.get_system_info`

```python
def get_system_info():
    """
    获取系统信息
    
    返回:
        dict: 系统信息，包括操作系统、shell类型、版本等
    """
```

### `ata.utils.safe_load_yaml`

```python
def safe_load_yaml(file_path):
    """
    安全加载YAML文件
    
    参数:
        file_path (str): 文件路径
        
    返回:
        dict: 加载的YAML数据，如果文件不存在或格式错误则返回空字典
    """
```

### `ata.utils.safe_dump_yaml`

```python
def safe_dump_yaml(data, file_path):
    """
    安全保存YAML文件
    
    参数:
        data (dict): 要保存的数据
        file_path (str): 文件路径
        
    返回:
        bool: 是否成功保存
    """
```

## 异常类

### `ata.exceptions.ATAError`

```python
class ATAError(Exception):
    """AI终端助手基础异常"""
    pass
```

### `ata.exceptions.APIError`

```python
class APIError(ATAError):
    """API错误异常"""
    pass
```

### `ata.exceptions.CommandError`

```python
class CommandError(ATAError):
    """命令错误异常"""
    pass
```

### `ata.exceptions.ConfigError`

```python
class ConfigError(ATAError):
    """配置错误异常"""
    pass
```

## 类型定义

### `ata.types.CommandData`

```python
CommandData = TypedDict('CommandData', {
    'success': bool,
    'command': Optional[str],
    'explanation': Optional[str],
    'warnings': List[str]
})
```

### `ata.types.ExecutionResult`

```python
ExecutionResult = TypedDict('ExecutionResult', {
    'success': bool,
    'exit_code': Optional[int],
    'stdout': str,
    'stderr': str,
    'duration': float
})
```

### `ata.types.SystemInfo`

```python
SystemInfo = TypedDict('SystemInfo', {
    'os': str,
    'shell': str,
    'version': str,
    'working_directory': str
})
```

## 示例

### 基本用法

```python
from ata.ai_interface import ModelFactory
from ata.command_executor import CommandExecutor
from ata.config_manager import ConfigManager

# 创建配置管理器
config_manager = ConfigManager()
config = config_manager.load()

# 获取默认提供商
provider = config.get("ai.provider", "openai")

# 创建AI模型接口
ai_interface = ModelFactory.create_model(
    provider=provider,
    api_key=None,  # 将从环境变量获取
    model=None,    # 将使用默认模型
    timeout=config.get("ai.timeout", 30)
)

# 创建命令执行器
command_executor = CommandExecutor(
    shell=config.get("execution.shell"),
    timeout=config.get("execution.timeout", 60)
)

# 获取系统信息
from ata.utils import get_system_info
system_info = get_system_info()

# 生成命令
user_input = "列出当前目录下的所有文件"
command_data = ai_interface.generate_command(user_input, system_info)

# 检查是否成功
if command_data["success"]:
    print(f"命令: {command_data['command']}")
    print(f"解释: {command_data['explanation']}")
    
    # 检查是否有警告
    if command_data["warnings"]:
        print("警告:")
        for warning in command_data["warnings"]:
            print(f"- {warning}")
    
    # 检查命令是否危险
    is_dangerous, warnings = command_executor.is_dangerous(command_data["command"])
    if is_dangerous:
        print("安全警告:")
        for warning in warnings:
            print(f"- {warning}")
    
    # 获取用户确认
    confirmation = input("是否执行此命令? (y/n): ")
    if confirmation.lower() == "y":
        # 执行命令
        result = command_executor.execute(command_data["command"])
        
        # 显示结果
        print(f"退出代码: {result['exit_code']}")
        if result["stdout"]:
            print("输出:")
            print(result["stdout"])
        if result["stderr"]:
            print("错误:")
            print(result["stderr"])
else:
    print("生成命令失败:")
    for warning in command_data["warnings"]:
        print(f"- {warning}")
```

### 使用自动回退机制

```python
from ata.ai_interface import ModelFactory
from ata.command_executor import CommandExecutor
import os

def process_with_fallback(user_input, system_info, primary_provider="openai", fallback_provider="deepseek"):
    """
    使用自动回退机制处理用户请求
    
    参数:
        user_input (str): 用户输入的自然语言请求
        system_info (dict): 系统信息
        primary_provider (str, 可选): 主要提供商。默认为"openai"。
        fallback_provider (str, 可选): 回退提供商。默认为"deepseek"。
        
    返回:
        dict: 命令数据
    """
    # 尝试使用主要提供商
    try:
        primary_interface = ModelFactory.create_model(provider=primary_provider)
        command_data = primary_interface.generate_command(user_input, system_info)
        
        # 如果成功生成命令，返回结果
        if command_data["success"]:
            return command_data
        
        print(f"使用{primary_provider}生成命令失败，尝试使用{fallback_provider}...")
    except Exception as e:
        print(f"使用{primary_provider}时出错: {str(e)}，尝试使用{fallback_provider}...")
    
    # 如果主要提供商失败，尝试使用回退提供商
    try:
        fallback_interface = ModelFactory.create_model(provider=fallback_provider)
        return fallback_interface.generate_command(user_input, system_info)
    except Exception as e:
        return {
            "success": False,
            "command": None,
            "explanation": None,
            "warnings": [f"所有提供商都失败: {str(e)}"]
        }

# 使用示例
if __name__ == "__main__":
    # 获取系统信息
    from ata.utils import get_system_info
    system_info = get_system_info()
    
    # 处理用户请求
    user_input = "列出当前目录下的所有文件"
    command_data = process_with_fallback(user_input, system_info)
    
    # 检查是否成功
    if command_data["success"]:
        print(f"命令: {command_data['command']}")
        print(f"解释: {command_data['explanation']}")
        
        # 执行命令
        command_executor = CommandExecutor()
        result = command_executor.execute(command_data["command"])
        
        # 显示结果
        print(f"输出: {result['stdout']}")
    else:
        print("生成命令失败:")
        for warning in command_data["warnings"]:
            print(f"- {warning}")
```

### 批处理模式

```python
from ata.ai_interface import ModelFactory
from ata.command_executor import CommandExecutor
import sys

def batch_process(file_path=None, auto_confirm=False, provider="openai"):
    """
    批处理模式
    
    参数:
        file_path (str, 可选): 请求文件路径。如果为None，将从标准输入读取。
        auto_confirm (bool, 可选): 是否自动确认执行命令。默认为False。
        provider (str, 可选): 使用的AI提供商。默认为"openai"。
    """
    # 创建AI模型接口和命令执行器
    ai_interface = ModelFactory.create_model(provider=provider)
    command_executor = CommandExecutor()
    
    # 获取系统信息
    from ata.utils import get_system_info
    system_info = get_system_info()
    
    # 读取请求
    if file_path:
        with open(file_path, "r") as f:
            requests = f.readlines()
    else:
        requests = sys.stdin.readlines()
    
    # 处理请求
    for request in requests:
        request = request.strip()
        if not request:
            continue
        
        print(f"处理请求: {request}")
        
        # 生成命令
        command_data = ai_interface.generate_command(request, system_info)
        
        # 检查是否成功
        if command_data["success"]:
            print(f"命令: {command_data['command']}")
            print(f"解释: {command_data['explanation']}")
            
            # 检查是否有警告
            if command_data["warnings"]:
                print("警告:")
                for warning in command_data["warnings"]:
                    print(f"- {warning}")
            
            # 检查命令是否危险
            is_dangerous, warnings = command_executor.is_dangerous(command_data["command"])
            if is_dangerous:
                print("安全警告:")
                for warning in warnings:
                    print(f"- {warning}")
                
                if not auto_confirm:
                    print("跳过危险命令")
                    continue
            
            # 获取用户确认
            if auto_confirm or input("是否执行此命令? (y/n): ").lower() == "y":
                # 执行命令
                result = command_executor.execute(command_data["command"])
                
                # 显示结果
                print(f"退出代码: {result['exit_code']}")
                if result["stdout"]:
                    print("输出:")
                    print(result["stdout"])
                if result["stderr"]:
                    print("错误:")
                    print(result["stderr"])
        else:
            print("生成命令失败:")
            for warning in command_data["warnings"]:
                print(f"- {warning}")
        
        print()

# 使用示例
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="AI终端助手批处理模式")
    parser.add_argument("--file", help="请求文件路径")
    parser.add_argument("--auto-confirm", action="store_true", help="自动确认执行命令")
    parser.add_argument("--provider", default="openai", choices=["openai", "deepseek"], help="使用的AI提供商")
    
    args = parser.parse_args()
    
    batch_process(args.file, args.auto_confirm, args.provider)
```

---

本文档提供了AI终端助手的API参考。如果你有任何问题，请参阅[开发者指南](developer_guide.md)或在[GitHub Issues](https://github.com/username/ai-terminal-assistant/issues)上提问。

