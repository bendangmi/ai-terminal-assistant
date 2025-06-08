# AI辅助终端程序技术规格

## 1. 技术栈详细规格

### 1.1 后端技术

| 组件 | 技术选择 | 版本 | 用途 |
|------|---------|------|------|
| 编程语言 | Python | 3.8+ | 主要开发语言 |
| AI API | OpenAI API | GPT-4o | 自然语言处理和命令生成 |
| 命令执行 | subprocess | 内置 | 执行系统命令 |
| 系统检测 | platform, os | 内置 | 检测操作系统和环境 |
| 配置管理 | configparser | 内置 | 管理用户配置 |
| HTTP客户端 | requests | 2.28+ | 与AI API通信 |
| 命令行界面 | argparse, rich | 内置, 13.0+ | 命令行参数处理和美化输出 |

### 1.2 前端技术（可选Web界面）

| 组件 | 技术选择 | 版本 | 用途 |
|------|---------|------|------|
| Web框架 | Flask | 2.2+ | 轻量级Web服务器 |
| 前端框架 | Vue.js | 3.0+ | 响应式用户界面 |
| CSS框架 | Tailwind CSS | 3.0+ | 界面样式 |
| WebSocket | Flask-SocketIO | 5.3+ | 实时通信 |

### 1.3 依赖项

```
# 核心依赖
openai>=1.0.0
requests>=2.28.0
rich>=13.0.0
pyyaml>=6.0

# Web界面依赖（可选）
flask>=2.2.0
flask-socketio>=5.3.0
```

## 2. 详细用户交互流程

### 2.1 命令行界面交互流程

```
+------------------+     +------------------+     +------------------+
|                  |     |                  |     |                  |
|  用户输入请求     | --> |  显示思考中状态   | --> |  展示生成的命令   |
|                  |     |                  |     |  和解释          |
+------------------+     +------------------+     +------------------+
                                                          |
                                                          v
+------------------+     +------------------+     +------------------+
|                  |     |                  |     |                  |
|  显示执行结果     | <-- |  执行命令        | <-- |  用户确认/编辑    |
|                  |     |                  |     |  命令            |
+------------------+     +------------------+     +------------------+
        |
        v
+------------------+
|                  |
|  等待下一个请求   |
|                  |
+------------------+
```

### 2.2 命令确认界面

```
生成的命令: find /var/log -type f -size +100M -exec ls -lh {} \;

解释: 这个命令会在/var/log目录下查找所有大于100MB的文件，并列出详细信息。

[!] 注意: 此命令将搜索系统日志目录，可能需要管理员权限。

选项:
[y] 执行命令
[n] 取消执行
[e] 编辑命令
[h] 显示帮助

请选择 (y/n/e/h):
```

### 2.3 命令编辑界面

```
原始命令: find /var/log -type f -size +100M -exec ls -lh {} \;

编辑命令: find /var/log -type f -size +100M -exec ls -lh {} \; | sort -k5,5hr

[Enter] 确认编辑
[Ctrl+C] 取消编辑
```

## 3. 模块接口设计

### 3.1 AI模型接口

```python
class AIModelInterface:
    def __init__(self, api_key, model="gpt-4o"):
        self.api_key = api_key
        self.model = model
        
    def generate_command(self, user_input, system_info, history=None):
        """
        根据用户输入生成命令
        
        参数:
            user_input (str): 用户的自然语言请求
            system_info (dict): 系统信息（操作系统、shell类型等）
            history (list, optional): 对话历史
            
        返回:
            dict: 包含生成的命令、解释和警告
        """
        # 实现与OpenAI API的交互
        pass
```

### 3.2 命令执行模块

```python
class CommandExecutor:
    def __init__(self, shell=None):
        self.shell = shell or self._detect_shell()
        
    def _detect_shell(self):
        """检测当前使用的shell"""
        pass
        
    def execute(self, command, timeout=30):
        """
        执行命令并返回结果
        
        参数:
            command (str): 要执行的命令
            timeout (int): 超时时间（秒）
            
        返回:
            dict: 包含执行状态、输出和错误信息
        """
        pass
        
    def is_dangerous(self, command):
        """
        检查命令是否危险
        
        参数:
            command (str): 要检查的命令
            
        返回:
            tuple: (是否危险, 警告信息)
        """
        pass
```

### 3.3 用户界面模块

```python
class CLI:
    def __init__(self, ai_interface, command_executor):
        self.ai_interface = ai_interface
        self.command_executor = command_executor
        
    def run(self):
        """启动命令行界面"""
        pass
        
    def process_request(self, user_input):
        """处理用户请求"""
        pass
        
    def display_command(self, command_data):
        """显示生成的命令和解释"""
        pass
        
    def get_confirmation(self, command, explanation, warnings=None):
        """获取用户确认"""
        pass
        
    def edit_command(self, command):
        """提供命令编辑功能"""
        pass
        
    def display_result(self, result):
        """显示命令执行结果"""
        pass
```

## 4. 数据流设计

### 4.1 用户请求处理流程

1. 用户输入自然语言请求
2. CLI模块接收请求并收集系统信息
3. 请求传递给AI模型接口
4. AI模型接口构建提示并调用OpenAI API
5. API返回生成的命令和解释
6. CLI模块显示命令和解释
7. 用户提供确认、编辑或取消
8. 如果确认，命令传递给命令执行模块
9. 命令执行模块执行命令并返回结果
10. CLI模块显示执行结果

### 4.2 数据结构

#### 4.2.1 用户请求

```json
{
  "input": "找出所有大于100MB的日志文件",
  "system_info": {
    "os": "Linux",
    "shell": "bash",
    "version": "5.4.0",
    "working_directory": "/home/user"
  },
  "history": [
    {"role": "user", "content": "如何查看系统内存使用情况"},
    {"role": "assistant", "content": "使用free -h命令可以查看系统内存使用情况"}
  ]
}
```

#### 4.2.2 AI响应

```json
{
  "command": "find /var/log -type f -size +100M -exec ls -lh {} \\;",
  "explanation": "这个命令会在/var/log目录下查找所有大于100MB的文件，并列出详细信息。",
  "warnings": ["此命令将搜索系统日志目录，可能需要管理员权限。"],
  "dangerous": false
}
```

#### 4.2.3 命令执行结果

```json
{
  "success": true,
  "exit_code": 0,
  "stdout": "-rw-r----- 1 syslog adm 124M Jun 7 10:30 /var/log/syslog.1\n-rw-r----- 1 syslog adm 156M Jun 7 11:45 /var/log/syslog",
  "stderr": "",
  "duration": 0.35
}
```

## 5. 配置管理

### 5.1 配置文件结构

```yaml
# ~/.ata/config.yaml
general:
  history_size: 20
  default_shell: auto  # auto, bash, zsh, powershell
  
ai:
  provider: openai
  model: gpt-4o
  api_key: ${OPENAI_API_KEY}  # 从环境变量读取
  temperature: 0.7
  
security:
  confirm_dangerous: true
  dangerous_patterns:
    - "rm -rf /*"
    - "dd.*of=/dev/"
    - ">.*/(passwd|shadow|group)"
  
ui:
  color_scheme: dark  # dark, light
  show_thinking: true
  command_timeout: 30
```

### 5.2 环境变量

- `OPENAI_API_KEY`: OpenAI API密钥
- `ATA_CONFIG_PATH`: 配置文件路径
- `ATA_HISTORY_PATH`: 历史记录文件路径
- `ATA_LOG_LEVEL`: 日志级别

## 6. 安全设计

### 6.1 命令安全检查规则

1. **危险命令模式**：使用正则表达式匹配已知的危险命令模式
2. **敏感目录操作**：检查是否操作系统关键目录（/etc, /bin, /sbin等）
3. **危险操作符**：检查是否包含危险的重定向操作符（> /dev/sda等）
4. **权限提升**：检查是否包含权限提升命令（sudo, su等）
5. **网络安全**：检查是否包含可能的网络攻击命令

### 6.2 API密钥保护

1. 优先从环境变量读取API密钥
2. 如果从配置文件读取，确保文件权限为600（仅所有者可读写）
3. 不在日志中记录API密钥
4. 提供API密钥验证功能，确保密钥有效

### 6.3 用户数据保护

1. 本地存储历史记录，不上传到服务器
2. 提供选项控制是否将系统信息发送到AI
3. 明确告知用户数据使用情况
4. 提供清除历史记录的功能

## 7. 错误处理

### 7.1 常见错误及处理方式

| 错误类型 | 处理方式 |
|---------|---------|
| API连接失败 | 重试连接，提供离线模式选项 |
| API密钥无效 | 提示用户更新API密钥 |
| 命令执行超时 | 允许用户取消或延长超时时间 |
| 命令执行错误 | 显示错误信息，提供修复建议 |
| 权限不足 | 提示用户使用sudo或提升权限 |

### 7.2 错误消息模板

```
[错误] API连接失败: 无法连接到OpenAI服务器
建议:
1. 检查网络连接
2. 确认API服务是否可用
3. 尝试稍后重试

是否重试连接? (y/n):
```

## 8. 测试策略

### 8.1 单元测试

- 测试AI模型接口的提示构建和响应解析
- 测试命令执行模块的命令执行和结果处理
- 测试安全检查模块的危险命令识别

### 8.2 集成测试

- 测试AI模型接口与命令执行模块的集成
- 测试用户界面与核心模块的集成
- 测试配置管理与各模块的集成

### 8.3 系统测试

- 测试完整的用户交互流程
- 测试不同操作系统环境下的兼容性
- 测试各种常见命令的生成和执行
- 测试错误处理和恢复机制

## 9. 部署和分发

### 9.1 打包方式

- 使用setuptools创建Python包
- 提供pip安装方式
- 为主要操作系统提供安装脚本

### 9.2 安装步骤

```bash
# 通过pip安装
pip install ai-terminal-assistant

# 设置API密钥
export OPENAI_API_KEY="your-api-key"

# 运行程序
ata "找出所有大于100MB的日志文件"
```

### 9.3 更新机制

- 通过pip更新
- 提供版本检查命令
- 保留用户配置和历史记录

## 10. 文档计划

### 10.1 用户文档

- 安装指南
- 快速入门
- 命令参考
- 配置指南
- 常见问题解答

### 10.2 开发者文档

- 架构概述
- API参考
- 扩展指南
- 贡献指南
- 测试指南

## 11. 项目时间线

| 阶段 | 任务 | 预计时间 |
|------|------|---------|
| 1 | 核心功能实现 | 2周 |
| 2 | 安全模块和命令编辑 | 1周 |
| 3 | 用户界面优化 | 1周 |
| 4 | 测试和bug修复 | 1周 |
| 5 | 文档和发布准备 | 1周 |

总计：约6周

