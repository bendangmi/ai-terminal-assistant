# AI终端助手 (ATA)

<div align="center">

![AI终端助手](https://via.placeholder.com/200x200?text=ATA)

[![PyPI version](https://img.shields.io/badge/pypi-v0.2.0-blue.svg)](https://pypi.org/project/ai-terminal-assistant/)
[![Python versions](https://img.shields.io/badge/python-3.8%2B-blue)](https://pypi.org/project/ai-terminal-assistant/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](https://github.com/username/ai-terminal-assistant/actions)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

</div>

AI终端助手（ATA）是一个基于人工智能的命令行工具，通过自然语言交互的方式帮助用户操作操作系统。用户只需用自然语言描述想要执行的操作，AI终端助手就会生成相应的命令，并在执行前请求用户确认，确保安全和可控。

## 特点

- **自然语言交互**：使用日常语言描述任务，无需记忆复杂命令
- **命令解释**：为每个生成的命令提供详细解释
- **安全检查**：自动检测潜在危险命令并提供警告
- **用户确认**：执行前需要用户确认，确保安全和可控
- **命令编辑**：允许用户在执行前编辑生成的命令
- **多模型支持**：支持OpenAI和DeepSeek等多种AI模型
- **自动回退机制**：当主要模型失败时自动切换到备用模型
- **跨平台支持**：支持Linux、macOS和Windows（实验性）

## 演示

![演示](https://via.placeholder.com/800x450?text=ATA+Demo)

```
$ ata "查找最近修改的大文件"
⠋ 思考中...
╭───────────────────────────────── 生成的命令 ─────────────────────────────────╮
│ find . -type f -size +10M -mtime -7 -exec ls -lh {} \;                       │
│                                                                              │
│ 解释:                                                                        │
│ 这个命令会在当前目录及其子目录中查找过去7天内修改过的大于10MB的文件，       │
│ 并以人类可读的格式显示文件详细信息。                                         │
│                                                                              │
╰──────────────────────────────────────────────────────────────────────────────╯
请选择 [y/n/e/h] (n): y
╭────────────────────────────────── 执行成功 ──────────────────────────────────╮
│ -rw-r--r-- 1 user user 25M Jun 5 10:23 ./downloads/dataset.zip              │
│ -rw-r--r-- 1 user user 15M Jun 6 14:45 ./documents/report.pdf               │
│ -rw-r--r-- 1 user user 42M Jun 7 09:12 ./videos/tutorial.mp4                │
│                                                                              │
│ 退出代码: 0, 执行时间: 0.35秒                                                │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## 安装

### 前提条件

- Python 3.8或更高版本
- OpenAI API密钥（使用OpenAI模型时）
- DeepSeek API密钥（使用DeepSeek模型时，可选）

### 使用pip安装

```bash
# 安装AI终端助手
pip install ai-terminal-assistant

# 设置API密钥
# OpenAI API密钥（默认模型提供商）
export OPENAI_API_KEY="your-openai-api-key"

# DeepSeek API密钥（可选）
export DEEPSEEK_API_KEY="your-deepseek-api-key"
```

### 从源代码安装

```bash
# 克隆仓库
git clone https://github.com/username/ai-terminal-assistant.git
cd ai-terminal-assistant

# 安装依赖
pip install -r requirements.txt

# 安装包
pip install -e .

# 设置API密钥
export OPENAI_API_KEY="your-openai-api-key"
export DEEPSEEK_API_KEY="your-deepseek-api-key"  # 可选
```

详细的安装说明请参阅[安装指南](docs/installation.md)。

## 使用方法

### 基本用法

```bash
# 基本用法
ata "列出当前目录下的所有文件"

# 或者进入交互模式
ata
```

### 命令行选项

```bash
# 显示帮助信息
ata --help

# 显示版本信息
ata --version

# 指定AI提供商
ata --provider openai "列出当前目录下的所有文件"
ata --provider deepseek "列出当前目录下的所有文件"

# 使用特定的AI模型
ata --model gpt-4o "列出当前目录下的所有文件"
ata --provider deepseek --model deepseek-v3-0324 "列出当前目录下的所有文件"

# 启用自动回退机制
ata --fallback "查找大文件"

# 指定回退提供商
ata --fallback --fallback-provider deepseek "查找大文件"

# 设置超时时间（秒）
ata --timeout 60 "查找大文件"

# 保存命令历史到文件
ata --history-file ~/.ata_history "列出进程"

# 显示模型性能统计
ata --stats

# 调试模式
ata --debug "检查系统信息"
```

详细的使用说明请参阅[用户手册](docs/user_manual.md)。

## 示例

### 文件操作

```bash
# 查找大文件
ata "查找大于100MB的文件"

# 批量重命名
ata "将当前目录下的所有.txt文件重命名为.md"

# 查找重复文件
ata "查找当前目录下的重复文件"
```

### 系统管理

```bash
# 查看系统信息
ata "显示系统信息"

# 管理进程
ata "查找占用内存最多的进程"

# 网络诊断
ata "检查网络连接问题"
```

### 开发工具

```bash
# Git操作
ata "查看最近的git提交"

# 代码搜索
ata "在所有Python文件中查找包含'error'的行"

# 环境设置
ata "设置Python虚拟环境"
```

### 多模型示例

```bash
# 使用OpenAI模型
ata --provider openai "查找大文件"

# 使用DeepSeek模型
ata --provider deepseek "查找大文件"

# 启用自动回退机制
ata --fallback "查找大文件"

# 比较不同模型的性能
ata --provider openai "查找大文件" && ata --provider deepseek "查找大文件"
```

更多示例请参阅[示例目录](examples/)。

## 文档

- [安装指南](docs/installation.md)
- [用户手册](docs/user_manual.md)
- [开发者指南](docs/developer_guide.md)
- [API参考](docs/api_reference.md)
- [常见问题](docs/faq.md)

## 贡献

我们欢迎所有形式的贡献，包括但不限于：

- 代码贡献
- 文档改进
- 错误报告
- 功能请求
- 代码审查

请参阅[开发者指南](docs/developer_guide.md)了解如何为项目做出贡献。

## 许可证

AI终端助手使用MIT许可证。详情请参阅[LICENSE](LICENSE)文件。

## 致谢

- [OpenAI](https://openai.com/) - 提供强大的语言模型
- [DeepSeek](https://deepseek.com/) - 提供高性能的替代模型
- [Rich](https://github.com/Textualize/rich) - 提供丰富的终端输出
- [所有贡献者](https://github.com/username/ai-terminal-assistant/graphs/contributors)

## 联系方式

- GitHub: [https://github.com/username/ai-terminal-assistant](https://github.com/username/ai-terminal-assistant)
- 电子邮件: example@example.com
- Discord: [https://discord.gg/example](https://discord.gg/example)

---

<div align="center">
  <sub>Built with ❤️ by the AI Terminal Assistant Team</sub>
</div>

