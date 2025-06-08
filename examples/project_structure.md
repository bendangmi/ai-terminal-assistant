# AI终端助手项目结构

本文档描述了AI终端助手（ATA）项目的目录结构和文件组织。

```
ai-terminal-assistant/
├── ata/                    # 主源代码目录
│   ├── __init__.py         # 包初始化文件，包含版本信息
│   ├── ai_interface.py     # AI模型接口，负责与OpenAI API通信
│   ├── cli.py              # 命令行界面，处理用户输入和显示结果
│   ├── command_executor.py # 命令执行模块，负责安全地执行命令
│   ├── config_manager.py   # 配置管理模块，负责加载和保存配置
│   ├── exceptions.py       # 异常类定义
│   ├── types.py            # 类型定义
│   └── utils.py            # 工具函数
│
├── docs/                   # 文档目录
│   ├── api_reference.md    # API参考文档
│   ├── developer_guide.md  # 开发者指南
│   ├── faq.md              # 常见问题
│   ├── installation.md     # 安装指南
│   ├── project_structure.md # 项目结构文档（本文件）
│   └── user_manual.md      # 用户手册
│
├── examples/               # 示例目录
│   ├── __init__.py         # 包初始化文件
│   ├── batch_processing.py # 批处理示例
│   ├── custom_provider.py  # 自定义AI提供商示例
│   ├── mock_test.py        # 模拟测试示例
│   ├── plugin_example.py   # 插件示例
│   └── simple_demo.py      # 简单演示示例
│
├── tests/                  # 测试目录
│   ├── __init__.py         # 包初始化文件
│   ├── test_ai_interface.py    # AI接口测试
│   ├── test_command_executor.py # 命令执行测试
│   ├── test_config_manager.py  # 配置管理测试
│   ├── test_integration.py     # 集成测试
│   └── test_utils.py           # 工具函数测试
│
├── .gitignore              # Git忽略文件
├── CHANGELOG.md            # 变更日志
├── LICENSE                 # 许可证文件
├── README.md               # 项目说明文件
├── pyproject.toml          # 项目配置文件
└── setup.py                # 安装脚本
```

## 主要模块说明

### `ata/ai_interface.py`

AI模型接口模块，负责与OpenAI API通信，将用户的自然语言请求转换为命令。主要功能包括：

- 构建API请求
- 解析API响应
- 处理错误和超时
- 提取命令和解释

### `ata/command_executor.py`

命令执行模块，负责安全地执行生成的命令并处理结果。主要功能包括：

- 检测命令是否危险
- 执行命令
- 处理超时和错误
- 格式化执行结果

### `ata/cli.py`

命令行界面模块，负责处理用户输入和显示结果。主要功能包括：

- 解析命令行参数
- 处理用户输入
- 显示命令和解释
- 获取用户确认
- 显示执行结果

### `ata/config_manager.py`

配置管理模块，负责加载和保存用户配置。主要功能包括：

- 加载配置文件
- 合并环境变量和默认值
- 验证配置
- 保存配置

### `ata/exceptions.py`

异常类定义模块，定义了项目中使用的自定义异常类。

### `ata/types.py`

类型定义模块，使用TypedDict定义了项目中使用的复杂数据类型。

### `ata/utils.py`

工具函数模块，包含各种辅助函数，如格式化持续时间、获取系统信息等。

## 文档目录

`docs/`目录包含项目的所有文档：

- `api_reference.md`: API参考文档，详细说明了项目的API接口
- `developer_guide.md`: 开发者指南，指导开发者如何为项目做出贡献
- `faq.md`: 常见问题，回答用户可能遇到的问题
- `installation.md`: 安装指南，详细说明了如何安装和配置项目
- `project_structure.md`: 项目结构文档（本文件）
- `user_manual.md`: 用户手册，详细说明了如何使用项目

## 示例目录

`examples/`目录包含各种示例，展示了如何使用项目的不同功能：

- `batch_processing.py`: 批处理示例，展示了如何批量处理请求
- `custom_provider.py`: 自定义AI提供商示例，展示了如何添加对其他AI提供商的支持
- `mock_test.py`: 模拟测试示例，使用mock来测试项目功能
- `plugin_example.py`: 插件示例，展示了如何创建和使用插件
- `simple_demo.py`: 简单演示示例，展示了项目的基本用法

## 测试目录

`tests/`目录包含项目的所有测试：

- `test_ai_interface.py`: AI接口测试，测试AI模型接口的功能
- `test_command_executor.py`: 命令执行测试，测试命令执行模块的功能
- `test_config_manager.py`: 配置管理测试，测试配置管理模块的功能
- `test_integration.py`: 集成测试，测试模块之间的交互
- `test_utils.py`: 工具函数测试，测试工具函数的功能

## 其他文件

- `.gitignore`: Git忽略文件，指定了不应该被Git跟踪的文件和目录
- `CHANGELOG.md`: 变更日志，记录了项目的版本历史和变更内容
- `LICENSE`: 许可证文件，指定了项目的许可条款
- `README.md`: 项目说明文件，提供了项目的概述和基本信息
- `pyproject.toml`: 项目配置文件，指定了项目的构建系统和依赖
- `setup.py`: 安装脚本，用于安装项目

## 配置文件

AI终端助手使用YAML格式的配置文件。默认配置文件位于`~/.ata/config.yaml`。配置文件的结构如下：

```yaml
# API设置
api:
  provider: openai
  key: your-api-key
  model: gpt-4o
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

## 环境变量

AI终端助手支持以下环境变量：

- `OPENAI_API_KEY`: OpenAI API密钥
- `ATA_CONFIG_FILE`: 配置文件路径
- `ATA_MODEL`: 默认AI模型
- `ATA_TIMEOUT`: API请求超时时间
- `ATA_EXECUTION_TIMEOUT`: 命令执行超时时间
- `ATA_HISTORY_FILE`: 命令历史文件路径
- `ATA_LOG_LEVEL`: 日志级别
- `ATA_LOG_FILE`: 日志文件路径
- `ATA_SHELL`: 指定shell

---

如果你有任何问题或建议，请参阅其他文档或在[GitHub Issues](https://github.com/username/ai-terminal-assistant/issues)上提问。

