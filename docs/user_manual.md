# AI终端助手 (ATA) 使用手册

## 目录

1. [项目概述](#项目概述)
2. [安装指南](#安装指南)
3. [使用方法](#使用方法)
4. [功能特点](#功能特点)
5. [安全考虑](#安全考虑)
6. [常见问题](#常见问题)
7. [高级用法](#高级用法)
8. [未来改进](#未来改进)
9. [贡献指南](#贡献指南)
10. [许可证](#许可证)

## 项目概述

AI终端助手（ATA）是一个基于人工智能的命令行工具，旨在通过自然语言交互的方式帮助用户操作操作系统。用户只需用自然语言描述想要执行的操作，AI终端助手就会生成相应的命令，并在执行前请求用户确认，确保安全和可控。

ATA利用先进的自然语言处理技术，将用户的自然语言请求转换为精确的命令行指令。它不仅能理解用户的意图，还能提供命令的解释和潜在风险警告，帮助用户更好地理解和使用命令行。

### 主要特点

- **自然语言交互**：使用日常语言描述任务，无需记忆复杂命令
- **多模型支持**：支持OpenAI和DeepSeek等多种AI模型，可根据需求选择
- **自动回退机制**：当首选模型失败时，自动切换到备用模型
- **命令解释**：为每个生成的命令提供详细解释
- **安全检查**：自动检测潜在危险命令并提供警告
- **用户确认**：执行前需要用户确认，确保安全和可控
- **命令编辑**：允许用户在执行前编辑生成的命令
- **跨平台支持**：支持Linux、macOS和Windows（实验性）

## 安装指南

### 系统要求

- Python 3.8或更高版本
- 互联网连接（用于与AI模型通信）
- OpenAI或DeepSeek API密钥

### 安装步骤

#### 1. 使用pip安装（推荐）

```bash
# 安装AI终端助手
pip install ai-terminal-assistant

# 设置API密钥（选择一个或两个都设置）
export OPENAI_API_KEY="your-openai-api-key"
export DEEPSEEK_API_KEY="your-deepseek-api-key"
```

#### 2. 从源代码安装

```bash
# 克隆仓库
git clone https://github.com/username/ai-terminal-assistant.git
cd ai-terminal-assistant

# 安装依赖
pip install -r requirements.txt

# 安装包
pip install -e .

# 设置API密钥（选择一个或两个都设置）
export OPENAI_API_KEY="your-openai-api-key"
export DEEPSEEK_API_KEY="your-deepseek-api-key"
```

### 验证安装

安装完成后，运行以下命令验证安装是否成功：

```bash
ata --version
```

如果安装成功，将显示版本信息。

## 使用方法

### 基本用法

AI终端助手可以通过命令行直接使用：

```bash
# 基本用法
ata "列出当前目录下的所有文件"

# 指定使用OpenAI模型
ata --provider openai "列出当前目录下的所有文件"

# 指定使用DeepSeek模型
ata --provider deepseek "列出当前目录下的所有文件"

# 或者进入交互模式
ata
```

### 交互模式

在交互模式下，你可以连续输入多个请求，而无需每次都输入`ata`命令：

```bash
$ ata --provider deepseek
ATA [DeepSeek]> 列出当前目录下的所有文件
[生成命令: ls -la]
[命令解释: 这个命令会列出当前目录下的所有文件，包括隐藏文件，并显示详细信息。]
是否执行此命令? (y/n/e - 执行/取消/编辑): y
[执行结果...]

ATA [DeepSeek]> 查找大于100MB的文件
[生成命令: find . -type f -size +100M]
[命令解释: 这个命令会在当前目录及其子目录中查找大于100MB的文件。]
是否执行此命令? (y/n/e - 执行/取消/编辑): y
[执行结果...]

ATA [DeepSeek]> 退出
再见！
```

### 命令行选项

AI终端助手支持多种命令行选项：

```bash
# 显示帮助信息
ata --help

# 显示版本信息
ata --version

# 指定AI提供商（openai或deepseek）
ata --provider deepseek "列出当前目录下的所有文件"

# 使用特定的AI模型（仅OpenAI）
ata --provider openai --model gpt-4 "列出当前目录下的所有文件"

# 设置超时时间（秒）
ata --timeout 60 "查找大文件"

# 启用自动回退机制
ata --auto-fallback "列出进程"

# 保存命令历史到文件
ata --history-file ~/.ata_history "列出进程"

# 调试模式
ata --debug "检查系统信息"
```

### 环境变量

AI终端助手支持以下环境变量：

- `OPENAI_API_KEY`：OpenAI API密钥（使用OpenAI模型时必需）
- `DEEPSEEK_API_KEY`：DeepSeek API密钥（使用DeepSeek模型时必需）
- `ATA_PROVIDER`：默认AI提供商（可选，默认为"openai"）
- `ATA_OPENAI_MODEL`：默认OpenAI模型（可选，默认为"gpt-4o"）
- `ATA_DEEPSEEK_MODEL`：默认DeepSeek模型（可选，默认为"deepseek-v3-0324"）
- `ATA_AUTO_FALLBACK`：启用自动回退机制（可选，默认为"false"）
- `ATA_FALLBACK_PROVIDER`：回退AI提供商（可选，默认为"deepseek"）
- `ATA_TIMEOUT`：默认超时时间（可选，默认为30秒）
- `ATA_HISTORY_FILE`：命令历史文件路径（可选）

## 功能特点

### 多模型支持

AI终端助手支持多种AI模型提供商，目前包括：

1. **OpenAI**：使用OpenAI的GPT模型，如gpt-4o、gpt-4-turbo等
2. **DeepSeek**：使用DeepSeek的模型，如deepseek-v3-0324、deepseek-r1-0528等

用户可以根据自己的需求和偏好选择不同的模型提供商。不同模型的特点如下：

| 提供商 | 模型 | 特点 | 适用场景 |
|-------|-----|------|---------|
| OpenAI | gpt-4o | 强大的通用能力，理解力强 | 复杂命令生成，需要深入理解的场景 |
| OpenAI | gpt-3.5-turbo | 速度快，成本低 | 简单命令生成，日常使用 |
| DeepSeek | deepseek-v3-0324 | 强大的推理能力，更好的代码理解 | 复杂脚本生成，开发相关任务 |
| DeepSeek | deepseek-r1-0528 | 改进的基准性能，减少幻觉 | 需要高精度的命令生成 |

### 自动回退机制

AI终端助手实现了自动回退机制，当首选模型失败时（如API错误、超时等），会自动切换到备用模型。这确保了即使在某个模型服务不可用的情况下，用户仍然可以使用AI终端助手。

自动回退流程：

1. 尝试使用首选模型（默认为OpenAI）生成命令
2. 如果失败，检查是否启用了自动回退机制
3. 如果启用，尝试使用备用模型（默认为DeepSeek）生成命令
4. 如果备用模型也失败，返回错误信息

### 自然语言处理

AI终端助手使用先进的AI模型将自然语言转换为命令。它能理解各种表达方式和意图，即使用户不知道确切的命令也能生成正确的指令。

示例：

| 自然语言请求 | 生成的命令 |
|------------|-----------|
| "列出当前目录下的所有文件" | `ls -la` |
| "查找大于100MB的文件" | `find . -type f -size +100M` |
| "显示系统内存使用情况" | `free -h` |
| "压缩当前目录下的所有图片文件" | `find . -type f \( -name "*.jpg" -o -name "*.png" \) -exec gzip {} \;` |

### 命令解释

对于每个生成的命令，AI终端助手都会提供详细的解释，帮助用户理解命令的作用和参数的含义。

### 安全检查

AI终端助手会自动检测潜在的危险命令，如删除系统文件、修改重要配置或需要提升权限的操作。对于这些命令，会显示警告信息并要求用户额外确认。

### 命令编辑

用户可以在执行前编辑生成的命令，这对于微调或修改生成的命令非常有用。

### 命令历史

AI终端助手会记录用户的请求和执行的命令，方便用户查看历史记录或重复执行之前的命令。

## 安全考虑

### 权限控制

AI终端助手不会自动提升权限。如果生成的命令需要管理员权限（如使用`sudo`），会显示警告并要求用户确认。

### 危险命令检测

以下类型的命令会被标记为潜在危险：

- 删除系统目录或文件（如`rm -rf /`）
- 修改系统配置文件
- 需要提升权限的命令（如`sudo`）
- 可能导致数据丢失的命令

### API密钥安全

API密钥是敏感信息，应妥善保管：

- 不要在公共代码或脚本中硬编码API密钥
- 使用环境变量或配置文件存储API密钥
- 定期轮换API密钥
- 设置适当的API使用限制

## 常见问题

### 命令生成失败

**问题**：AI终端助手无法生成命令或生成的命令不正确。

**解决方案**：
- 尝试更详细地描述你想要执行的操作
- 检查网络连接是否正常
- 确认API密钥是否有效
- 尝试切换到其他AI提供商（如`--provider deepseek`）
- 尝试使用更高级的AI模型（如`--model gpt-4`）

### API密钥问题

**问题**：出现"API密钥未提供"或"API密钥无效"的错误。

**解决方案**：
- 确认已正确设置相应的API密钥环境变量（`OPENAI_API_KEY`或`DEEPSEEK_API_KEY`）
- 检查API密钥是否有效
- 确认API密钥有足够的配额

### 命令执行超时

**问题**：执行命令时出现超时错误。

**解决方案**：
- 使用`--timeout`选项增加超时时间
- 对于长时间运行的命令，考虑使用`nohup`或`screen`等工具

### 不支持的操作系统

**问题**：在不支持的操作系统上使用AI终端助手。

**解决方案**：
- 确认你的操作系统是否受支持（Linux、macOS或Windows）
- 在Windows上，确保使用WSL（Windows Subsystem for Linux）或Git Bash等兼容环境

### 模型切换问题

**问题**：无法切换到指定的AI模型提供商。

**解决方案**：
- 确认已设置相应的API密钥
- 检查拼写是否正确（`openai`或`deepseek`）
- 尝试使用环境变量设置默认提供商

## 高级用法

### 自定义提示模板

高级用户可以自定义提示模板，以改变AI终端助手生成命令的方式：

```bash
# 使用自定义提示模板
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

### 模型性能监控

AI终端助手可以记录不同模型的性能指标，帮助用户选择最适合自己需求的模型：

```bash
# 启用性能监控
ata --enable-metrics "列出文件"

# 查看性能报告
ata --show-metrics
```

性能报告示例：

```
模型性能报告：
+----------------+------------+----------------+---------------+
| 提供商         | 平均响应时间 | 成功率         | 命令准确率     |
+----------------+------------+----------------+---------------+
| OpenAI (gpt-4o)| 2.3秒      | 98.5%          | 95.2%         |
| DeepSeek (v3)  | 1.8秒      | 97.2%          | 93.8%         |
+----------------+------------+----------------+---------------+
```

### 集成到其他工具

AI终端助手可以作为库集成到其他Python项目中：

```python
from ata.ai_interface import AIModelInterface
from ata.command_executor import CommandExecutor

# 创建AI模型接口（可以选择提供商）
ai_interface = AIModelInterface(provider="deepseek", api_key="your-api-key")

# 创建命令执行器
command_executor = CommandExecutor()

# 生成命令
system_info = {
    "os": "Linux",
    "shell": "bash",
    "working_directory": "/home/user"
}
result = ai_interface.generate_command("列出所有正在运行的进程", system_info)

# 显示命令和解释
print(f"命令: {result['command']}")
print(f"解释: {result['explanation']}")

# 执行命令
if input("是否执行此命令? (y/n): ").lower() == "y":
    execution_result = command_executor.execute(result["command"])
    print(execution_result["stdout"])
```

### 批处理模式

对于需要批量处理的场景，可以使用批处理模式：

```bash
# 从文件读取请求并执行
ata --batch-file requests.txt --auto-confirm

# 或者通过管道传入请求
cat requests.txt | ata --batch --auto-confirm

# 指定使用DeepSeek模型进行批处理
ata --provider deepseek --batch-file requests.txt --auto-confirm
```

## 未来改进

AI终端助手仍在积极开发中，计划的未来改进包括：

1. **更多AI模型支持**：添加对更多模型提供商和本地模型的支持
2. **命令历史分析**：基于历史命令提供更智能的建议
3. **自定义别名**：允许用户为常用操作创建自然语言别名
4. **多语言支持**：添加对更多语言的支持
5. **图形用户界面**：提供基于Web或桌面的图形界面
6. **插件系统**：允许用户扩展功能
7. **离线模式**：支持在没有互联网连接的情况下使用
8. **命令学习**：从用户交互中学习和改进
9. **模型自动选择**：根据任务类型自动选择最适合的模型

## 贡献指南

我们欢迎社区贡献！如果你想为AI终端助手做出贡献，请遵循以下步骤：

1. Fork仓库
2. 创建功能分支（`git checkout -b feature/amazing-feature`）
3. 提交更改（`git commit -m 'Add some amazing feature'`）
4. 推送到分支（`git push origin feature/amazing-feature`）
5. 创建Pull Request

### 开发环境设置

```bash
# 克隆仓库
git clone https://github.com/username/ai-terminal-assistant.git
cd ai-terminal-assistant

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # 在Windows上使用 venv\Scripts\activate

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
python -m unittest discover tests
```

## 许可证

AI终端助手使用MIT许可证。详情请参阅[LICENSE](../LICENSE)文件。

---

© 2025 AI Terminal Assistant Team

