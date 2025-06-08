# AI终端助手安装指南

本文档提供了详细的AI终端助手（ATA）安装和配置说明。

## 目录

1. [系统要求](#系统要求)
2. [安装方法](#安装方法)
   - [使用pip安装](#使用pip安装)
   - [从源代码安装](#从源代码安装)
   - [Docker安装](#docker安装)
3. [配置](#配置)
   - [API密钥设置](#api密钥设置)
   - [配置文件](#配置文件)
   - [环境变量](#环境变量)
4. [验证安装](#验证安装)
5. [故障排除](#故障排除)
6. [卸载](#卸载)

## 系统要求

在安装AI终端助手之前，请确保您的系统满足以下要求：

- **操作系统**：
  - Linux（推荐Ubuntu 20.04+、Debian 11+、CentOS 8+）
  - macOS 11.0+
  - Windows 10/11（实验性支持，推荐使用WSL）

- **Python**：
  - Python 3.8或更高版本
  - pip 20.0或更高版本

- **硬件**：
  - 最低：1GB RAM，1GB可用磁盘空间
  - 推荐：4GB RAM，2GB可用磁盘空间

- **网络**：
  - 稳定的互联网连接（用于与AI API通信）

- **其他**：
  - OpenAI API密钥（使用OpenAI模型时必需）
  - DeepSeek API密钥（使用DeepSeek模型时必需）

## 安装方法

### 使用pip安装

使用pip安装是最简单的方法，适用于大多数用户：

```bash
# 安装最新稳定版
pip install ai-terminal-assistant

# 或者安装特定版本
pip install ai-terminal-assistant==0.2.0

# 如果你想安装开发版本
pip install git+https://github.com/username/ai-terminal-assistant.git
```

### 从源代码安装

如果你想从源代码安装，或者想要修改代码，可以按照以下步骤操作：

```bash
# 克隆仓库
git clone https://github.com/username/ai-terminal-assistant.git
cd ai-terminal-assistant

# 创建虚拟环境（可选但推荐）
python -m venv venv
source venv/bin/activate  # 在Windows上使用 venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 安装包
pip install -e .
```

### Docker安装

如果你喜欢使用Docker，可以使用以下命令：

```bash
# 拉取镜像
docker pull username/ai-terminal-assistant:latest

# 运行容器（使用OpenAI）
docker run -it --rm \
  -e OPENAI_API_KEY="your-openai-api-key" \
  username/ai-terminal-assistant:latest

# 或者使用DeepSeek
docker run -it --rm \
  -e DEEPSEEK_API_KEY="your-deepseek-api-key" \
  -e ATA_PROVIDER="deepseek" \
  username/ai-terminal-assistant:latest
```

或者，你可以使用提供的Dockerfile自己构建镜像：

```bash
# 克隆仓库
git clone https://github.com/username/ai-terminal-assistant.git
cd ai-terminal-assistant

# 构建镜像
docker build -t ai-terminal-assistant .

# 运行容器
docker run -it --rm \
  -e OPENAI_API_KEY="your-openai-api-key" \
  -e DEEPSEEK_API_KEY="your-deepseek-api-key" \
  ai-terminal-assistant
```

## 配置

### API密钥设置

AI终端助手需要AI模型提供商的API密钥才能工作。你可以通过以下方式设置API密钥：

1. **环境变量**（推荐）：

   ```bash
   # OpenAI API密钥（使用OpenAI模型时必需）
   # Linux/macOS
   export OPENAI_API_KEY="your-openai-api-key"
   
   # Windows (CMD)
   set OPENAI_API_KEY=your-openai-api-key
   
   # Windows (PowerShell)
   $env:OPENAI_API_KEY="your-openai-api-key"
   
   # DeepSeek API密钥（使用DeepSeek模型时必需）
   # Linux/macOS
   export DEEPSEEK_API_KEY="your-deepseek-api-key"
   
   # Windows (CMD)
   set DEEPSEEK_API_KEY=your-deepseek-api-key
   
   # Windows (PowerShell)
   $env:DEEPSEEK_API_KEY="your-deepseek-api-key"
   ```

2. **配置文件**：

   创建或编辑`~/.ata/config.yaml`文件：

   ```yaml
   # OpenAI配置
   openai:
     api_key: your-openai-api-key
     model: gpt-4o
   
   # DeepSeek配置
   deepseek:
     api_key: your-deepseek-api-key
     model: deepseek-v3-0324
   
   # 默认提供商
   ai:
     provider: openai
     auto_fallback: true
     fallback_provider: deepseek
   ```

3. **命令行参数**：

   ```bash
   # 使用OpenAI
   ata --provider openai --api-key "your-openai-api-key" "列出文件"
   
   # 使用DeepSeek
   ata --provider deepseek --api-key "your-deepseek-api-key" "列出文件"
   ```

### 配置文件

AI终端助手使用YAML格式的配置文件。默认配置文件位于`~/.ata/config.yaml`。你可以创建或编辑此文件来自定义AI终端助手的行为。

示例配置文件：

```yaml
# AI设置
ai:
  provider: openai
  auto_fallback: true
  fallback_provider: deepseek

# OpenAI设置
openai:
  api_key: your-openai-api-key
  model: gpt-4o
  timeout: 30

# DeepSeek设置
deepseek:
  api_key: your-deepseek-api-key
  model: deepseek-v3-0324
  timeout: 30

# 命令执行设置
execution:
  timeout: 60
  shell: auto
  confirm_dangerous: true
  dangerous_patterns:
    - rm\s+-rf\s+/
    - sudo\s+
    - chmod\s+777

# 用户界面设置
ui:
  color: true
  verbose: false
  history_file: ~/.ata_history
  max_history: 100

# 日志设置
logging:
  level: info
  file: ~/.ata/ata.log
  max_size: 10MB
  backup_count: 3
```

### 环境变量

AI终端助手支持以下环境变量：

| 环境变量 | 描述 | 默认值 |
|---------|------|-------|
| `OPENAI_API_KEY` | OpenAI API密钥 | 无（使用OpenAI时必需） |
| `DEEPSEEK_API_KEY` | DeepSeek API密钥 | 无（使用DeepSeek时必需） |
| `ATA_CONFIG_FILE` | 配置文件路径 | `~/.ata/config.yaml` |
| `ATA_PROVIDER` | 默认AI提供商 | `openai` |
| `ATA_AUTO_FALLBACK` | 启用自动回退机制 | `false` |
| `ATA_FALLBACK_PROVIDER` | 回退AI提供商 | `deepseek` |
| `ATA_OPENAI_MODEL` | 默认OpenAI模型 | `gpt-4o` |
| `ATA_DEEPSEEK_MODEL` | 默认DeepSeek模型 | `deepseek-v3-0324` |
| `ATA_TIMEOUT` | API请求超时时间（秒） | `30` |
| `ATA_EXECUTION_TIMEOUT` | 命令执行超时时间（秒） | `60` |
| `ATA_HISTORY_FILE` | 命令历史文件路径 | `~/.ata_history` |
| `ATA_LOG_LEVEL` | 日志级别 | `info` |
| `ATA_LOG_FILE` | 日志文件路径 | `~/.ata/ata.log` |
| `ATA_SHELL` | 指定shell | `auto` |

## 验证安装

安装完成后，可以运行以下命令验证安装是否成功：

```bash
# 显示版本信息
ata --version

# 运行简单测试（使用OpenAI）
ata --provider openai "echo 'Hello, World!'"

# 运行简单测试（使用DeepSeek）
ata --provider deepseek "echo 'Hello, World!'"
```

如果一切正常，你应该能看到版本信息和命令执行结果。

## 故障排除

如果你在安装或使用AI终端助手时遇到问题，请尝试以下解决方案：

### 常见问题

1. **找不到命令**

   ```
   bash: ata: command not found
   ```

   **解决方案**：
   - 确保Python的bin目录在PATH中
   - 尝试使用完整路径运行：`python -m ata`
   - 重新安装：`pip install --force-reinstall ai-terminal-assistant`

2. **API密钥错误**

   ```
   Error: API密钥未提供。请设置相应的API密钥环境变量或在配置文件中提供api_key。
   ```

   **解决方案**：
   - 检查是否正确设置了相应的API密钥环境变量（`OPENAI_API_KEY`或`DEEPSEEK_API_KEY`）
   - 确认API密钥格式正确
   - 尝试在配置文件中设置API密钥

3. **提供商错误**

   ```
   Error: 无效的AI提供商。支持的提供商有：openai, deepseek
   ```

   **解决方案**：
   - 检查提供商名称拼写是否正确
   - 确保使用小写字母
   - 尝试使用默认提供商（不指定`--provider`选项）

4. **依赖冲突**

   ```
   ERROR: pip's dependency resolver does not currently take into account all the packages that are installed...
   ```

   **解决方案**：
   - 在虚拟环境中安装
   - 使用`pip install --ignore-installed ai-terminal-assistant`
   - 更新pip：`pip install --upgrade pip`

5. **超时错误**

   ```
   Error: API请求超时
   ```

   **解决方案**：
   - 检查网络连接
   - 增加超时时间：`ata --timeout 60`
   - 检查API服务状态
   - 尝试切换到另一个提供商：`ata --provider deepseek`

### 日志文件

如果问题仍然存在，可以查看日志文件获取更多信息：

```bash
# 显示日志文件的最后20行
tail -n 20 ~/.ata/ata.log

# 以调试模式运行
ata --debug "列出文件"
```

### 获取帮助

如果你无法解决问题，可以：

- 查看[GitHub Issues](https://github.com/username/ai-terminal-assistant/issues)
- 创建新的Issue，提供详细的错误信息和复现步骤
- 加入[Discord社区](https://discord.gg/example)寻求帮助

## 卸载

如果你想卸载AI终端助手，可以使用以下命令：

```bash
# 使用pip卸载
pip uninstall ai-terminal-assistant

# 删除配置文件和日志（可选）
rm -rf ~/.ata
rm ~/.ata_history
```

---

如果你有任何问题或建议，请随时联系我们。

