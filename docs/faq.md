# AI终端助手常见问题 (FAQ)

本文档回答了关于AI终端助手（ATA）的常见问题。

## 目录

1. [基本问题](#基本问题)
2. [安装问题](#安装问题)
3. [使用问题](#使用问题)
4. [安全问题](#安全问题)
5. [性能问题](#性能问题)
6. [API问题](#api问题)
7. [高级问题](#高级问题)
8. [故障排除](#故障排除)

## 基本问题

### 什么是AI终端助手？

AI终端助手（ATA）是一个基于人工智能的命令行工具，通过自然语言交互的方式帮助用户操作操作系统。用户只需用自然语言描述想要执行的操作，AI终端助手就会生成相应的命令，并在执行前请求用户确认，确保安全和可控。

### AI终端助手支持哪些操作系统？

AI终端助手主要支持Linux和macOS操作系统。对Windows的支持处于实验阶段，建议在Windows上使用WSL（Windows Subsystem for Linux）或Git Bash等兼容环境。

### AI终端助手是免费的吗？

AI终端助手本身是开源免费的，但它依赖于OpenAI API，这需要API密钥和可能的使用费用。OpenAI提供一定的免费额度，但超出部分需要付费。

### AI终端助手需要联网吗？

是的，AI终端助手需要互联网连接来与OpenAI API通信。目前不支持完全离线使用。

## 安装问题

### 如何安装AI终端助手？

最简单的安装方法是使用pip：

```bash
pip install ai-terminal-assistant
```

详细的安装说明请参阅[安装指南](installation.md)。

### 为什么安装后找不到`ata`命令？

这可能是因为Python的bin目录不在你的PATH环境变量中。尝试以下解决方案：

1. 使用完整路径运行：`python -m ata`
2. 将Python的bin目录添加到PATH中
3. 重新安装：`pip install --user ai-terminal-assistant`

### 如何更新AI终端助手？

使用pip更新：

```bash
pip install --upgrade ai-terminal-assistant
```

### 如何卸载AI终端助手？

使用pip卸载：

```bash
pip uninstall ai-terminal-assistant
```

如果你想完全删除所有配置和数据，还可以删除`~/.ata`目录和`~/.ata_history`文件。

## 使用问题

### 如何使用AI终端助手？

基本用法：

```bash
# 直接使用
ata "列出当前目录下的所有文件"

# 交互模式
ata
```

详细的使用说明请参阅[用户手册](user_manual.md)。

### 如何设置OpenAI API密钥？

有几种方式设置API密钥：

1. 环境变量（推荐）：
   ```bash
   export OPENAI_API_KEY="your-api-key"
   ```

2. 配置文件：
   在`~/.ata/config.yaml`中设置：
   ```yaml
   api:
     key: your-api-key
   ```

3. 命令行参数：
   ```bash
   ata --api-key "your-api-key" "列出文件"
   ```

### 如何使用交互模式？

启动交互模式：

```bash
ata
```

在交互模式下，你可以连续输入多个请求，而无需每次都输入`ata`命令。输入`exit`或`quit`退出交互模式。

### 如何查看命令历史？

使用`--history`选项查看命令历史：

```bash
ata --history
```

或者直接查看历史文件：

```bash
cat ~/.ata_history
```

### 如何保存命令历史到特定文件？

使用`--history-file`选项：

```bash
ata --history-file ~/my_commands.txt "列出文件"
```

### 如何使用不同的AI模型？

使用`--model`选项：

```bash
ata --model gpt-4 "列出文件"
```

或者在配置文件中设置默认模型：

```yaml
api:
  model: gpt-4
```

### 如何增加超时时间？

使用`--timeout`选项：

```bash
ata --timeout 60 "查找大文件"
```

或者在配置文件中设置默认超时时间：

```yaml
api:
  timeout: 60
```

## 安全问题

### AI终端助手如何保证安全？

AI终端助手采取了多种安全措施：

1. 命令确认机制：在执行任何命令前都会请求用户确认
2. 危险命令检测：自动检测潜在危险的命令并提供警告
3. 权限提升警告：对需要提升权限的命令（如使用`sudo`）发出警告
4. 命令编辑：允许用户在执行前编辑生成的命令
5. 超时机制：防止长时间运行的命令

### AI终端助手会自动执行危险命令吗？

不会。AI终端助手会检测潜在危险的命令，并在执行前显示警告和请求用户确认。用户必须明确确认才会执行命令。

### 我的API密钥安全吗？

AI终端助手不会将你的API密钥发送到除OpenAI之外的任何服务器。API密钥存储在本地配置文件中，建议设置适当的文件权限（如`chmod 600 ~/.ata/config.yaml`）。

### AI终端助手会收集我的数据吗？

AI终端助手本身不会收集或上传你的数据。但是，你的请求和系统信息会发送到OpenAI进行处理。请查阅[OpenAI的隐私政策](https://openai.com/privacy/)了解更多信息。

## 性能问题

### 为什么AI终端助手有时响应很慢？

响应速度主要受以下因素影响：

1. 网络连接质量
2. OpenAI API的负载和响应时间
3. 请求的复杂性
4. 选择的AI模型（如gpt-4通常比gpt-3.5-turbo慢）

### 如何提高AI终端助手的响应速度？

尝试以下方法：

1. 使用更快的AI模型：`ata --model gpt-3.5-turbo`
2. 减少超时时间：`ata --timeout 10`
3. 确保良好的网络连接
4. 使用简洁明确的请求

### AI终端助手使用多少内存？

AI终端助手本身的内存占用很小，通常不超过50MB。但是，执行的命令可能会使用更多内存，具体取决于命令的性质。

## API问题

### 如何获取OpenAI API密钥？

1. 访问[OpenAI API网站](https://platform.openai.com/)
2. 创建或登录账户
3. 导航到API密钥部分
4. 创建新的API密钥

### 使用AI终端助手会消耗多少API额度？

每次请求的API使用量取决于以下因素：

1. 选择的AI模型
2. 请求的长度
3. 生成的响应长度

一般来说，一个简单的命令生成请求消耗的token数量在500-1500之间。

### 如何查看我的API使用情况？

访问[OpenAI API使用页面](https://platform.openai.com/usage)查看你的API使用情况和剩余额度。

### 如何设置API使用限制？

访问[OpenAI API限制页面](https://platform.openai.com/account/limits)设置API使用限制，防止意外超额使用。

## 高级问题

### 如何自定义提示模板？

创建一个自定义提示模板文件，然后使用`--prompt-template`选项：

```bash
ata --prompt-template /path/to/template.txt "列出文件"
```

模板文件示例：

```
你是一个命令行专家，请根据用户的请求生成适合{os}系统的命令。
用户的工作目录是：{working_directory}
用户的shell是：{shell}

用户请求：{user_input}

请生成命令并解释其作用。
```

### 如何将AI终端助手集成到其他工具中？

AI终端助手可以作为库集成到其他Python项目中：

```python
from ata.ai_interface import AIModelInterface
from ata.command_executor import CommandExecutor

# 创建AI模型接口
ai_interface = AIModelInterface(api_key="your-api-key")

# 创建命令执行器
command_executor = CommandExecutor()

# 生成命令
result = ai_interface.generate_command("列出文件", {"os": "Linux"})

# 执行命令
execution_result = command_executor.execute(result["command"])
```

### 如何添加自定义命令模式？

在配置文件中添加自定义的危险命令模式：

```yaml
execution:
  dangerous_patterns:
    - rm\s+-rf\s+/
    - sudo\s+
    - chmod\s+777
    - mv\s+\/\w+
    - >-
      # 自定义模式
      dd\s+if=.+\s+of=/dev/
```

### 如何使用批处理模式？

使用`--batch-file`选项从文件读取请求：

```bash
# 创建请求文件
echo "列出文件" > requests.txt
echo "显示内存使用" >> requests.txt

# 执行批处理
ata --batch-file requests.txt --auto-confirm
```

或者通过管道传入请求：

```bash
cat requests.txt | ata --batch --auto-confirm
```

## 故障排除

### 为什么我收到"API密钥无效"错误？

可能的原因：

1. API密钥不正确或已过期
2. API密钥格式错误（应以"sk-"开头）
3. API密钥没有正确设置（检查环境变量或配置文件）

解决方案：

1. 在OpenAI网站上验证API密钥
2. 生成新的API密钥
3. 确保正确设置环境变量：`export OPENAI_API_KEY="your-api-key"`

### 为什么命令生成失败？

可能的原因：

1. 网络连接问题
2. API请求超时
3. 请求不明确或太复杂
4. API额度用尽

解决方案：

1. 检查网络连接
2. 增加超时时间：`ata --timeout 60`
3. 使用更明确的请求
4. 检查API使用情况和额度

### 为什么生成的命令不正确？

可能的原因：

1. 请求不明确或有歧义
2. AI模型的限制
3. 系统信息不足

解决方案：

1. 使用更明确的请求
2. 尝试更高级的AI模型：`ata --model gpt-4`
3. 提供更多上下文信息

### 如何查看调试信息？

使用`--debug`选项启用调试模式：

```bash
ata --debug "列出文件"
```

或者设置日志级别：

```bash
ata --log-level debug "列出文件"
```

### 如何报告问题？

如果你遇到问题，请在[GitHub Issues](https://github.com/username/ai-terminal-assistant/issues)上报告，并提供以下信息：

1. AI终端助手版本（`ata --version`）
2. 操作系统和版本
3. Python版本
4. 错误消息和日志
5. 复现步骤

---

如果你有其他问题，请查阅[用户手册](user_manual.md)或[开发者指南](developer_guide.md)，或者在[GitHub Issues](https://github.com/username/ai-terminal-assistant/issues)上提问。

