# AI终端助手项目目录结构

```
ai-terminal-assistant/              # 项目根目录
│
├── ata/                            # 主源代码目录
│   ├── __init__.py                 # 包初始化文件
│   ├── ai_interface.py             # AI模型接口模块
│   ├── cli.py                      # 命令行界面模块
│   ├── command_executor.py         # 命令执行模块
│   └── config_manager.py           # 配置管理模块
│
├── docs/                           # 文档目录
│   ├── README.md                   # 文档目录说明
│   ├── api_reference.md            # API参考文档
│   ├── developer_guide.md          # 开发者指南
│   ├── faq.md                      # 常见问题
│   ├── installation.md             # 安装指南
│   ├── optimization_summary.md     # 优化项目总结文档
│   ├── project_structure.md        # 项目结构文档
│   ├── project_summary.md          # 项目总结文档
│   └── user_manual.md              # 用户手册
│
├── examples/                       # 示例目录
│   ├── README.md                   # 示例目录说明
│   ├── __init__.py                 # 包初始化文件
│   ├── mock_test.py                # 模拟测试示例
│   └── simple_demo.py              # 简单演示示例
│
├── tests/                          # 测试目录
│   ├── README.md                   # 测试目录说明
│   ├── __init__.py                 # 包初始化文件
│   ├── test_ai_interface.py        # AI模型接口测试
│   └── test_command_executor.py    # 命令执行模块测试
│
├── .gitignore                      # Git忽略文件
├── CHANGELOG.md                    # 变更日志
├── LICENSE                         # 许可证文件
├── README.md                       # 项目说明文件
└── setup.py                        # 安装配置文件
```

## 核心文件说明

### 源代码文件

- **ata/__init__.py**: 包初始化文件，定义版本号
- **ata/ai_interface.py**: AI模型接口模块，负责与AI服务通信，将用户请求转换为命令
- **ata/cli.py**: 命令行界面模块，负责处理用户输入和显示结果
- **ata/command_executor.py**: 命令执行模块，负责执行生成的命令并处理结果
- **ata/config_manager.py**: 配置管理模块，负责加载和保存用户配置

### 文档文件

- **docs/api_reference.md**: API参考文档，详细说明各个模块的类和方法
- **docs/developer_guide.md**: 开发者指南，说明如何为项目做出贡献和扩展功能
- **docs/installation.md**: 安装指南，详细说明如何安装和配置AI终端助手
- **docs/optimization_summary.md**: 优化项目总结文档，总结引入DeepSeek模型的优化结果
- **docs/user_manual.md**: 用户手册，详细说明如何使用AI终端助手

### 示例文件

- **examples/mock_test.py**: 模拟测试示例，使用模拟数据测试AI终端助手的功能
- **examples/simple_demo.py**: 简单演示示例，展示AI终端助手的基本用法

### 测试文件

- **tests/test_ai_interface.py**: AI模型接口测试，测试AI模型接口的功能
- **tests/test_command_executor.py**: 命令执行模块测试，测试命令执行模块的功能

### 其他文件

- **README.md**: 项目说明文件，提供项目概述、特点、安装和使用说明
- **setup.py**: 安装配置文件，定义项目的依赖项和安装方式
- **LICENSE**: 许可证文件，使用MIT许可证
- **CHANGELOG.md**: 变更日志，记录项目的版本历史和变更内容


# AI终端助手测试

本目录包含AI终端助手的测试文件。

## 运行测试

可以使用以下命令运行所有测试：

```bash
# 在项目根目录下运行
python -m unittest discover tests

# 或者使用pytest
pytest
```

## 运行单个测试文件

```bash
# 运行AI模型接口测试
python -m unittest tests/test_ai_interface.py

# 运行命令执行模块测试
python -m unittest tests/test_command_executor.py
```

## 测试覆盖范围

当前测试覆盖以下模块：

1. `ai_interface.py` - AI模型接口
   - 测试生成命令功能
   - 测试解析响应功能
   - 测试错误处理

2. `command_executor.py` - 命令执行模块
   - 测试检测shell类型
   - 测试执行命令
   - 测试命令执行错误处理
   - 测试危险命令检测

## 添加新测试

添加新测试时，请遵循以下命名约定：

- 测试文件名应以`test_`开头
- 测试类名应以`Test`开头
- 测试方法名应以`test_`开头

例如：

```python
# tests/test_new_module.py
import unittest

class TestNewModule(unittest.TestCase):
    def test_some_function(self):
        # 测试代码
        pass
```

