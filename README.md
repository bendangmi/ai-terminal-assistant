# AI Terminal Assistant

一个基于Python和Vue的智能终端助手系统。

## 项目结构

```
ai-terminal-assistant/
├── ata/                    # 后端Python包
│   ├── api/               # API模块
│   │   ├── __init__.py
│   │   ├── system_info.py
│   │   ├── connection_test.py
│   │   └── config_api.py
│   ├── __init__.py
│   ├── config_manager.py
│   ├── command_executor.py
│   └── web_server.py
├── web/                    # 前端Vue项目
│   ├── src/
│   │   ├── components/
│   │   ├── assets/
│   │   ├── App.vue
│   │   └── main.js
│   ├── public/
│   ├── package.json
│   └── vite.config.js
├── config.yaml            # 配置文件
├── requirements.txt       # Python依赖
└── README.md             # 项目文档
```

## 功能特性

- 系统监控
  - CPU使用率监控
  - 内存使用情况
  - 磁盘使用状态
  - 文件系统浏览
- 服务器管理
  - 服务器连接配置
  - 连接状态测试
  - 服务器性能监控
- AI配置
  - 多AI提供商支持（DeepSeek、OpenAI）
  - API密钥管理
  - 模型参数配置
- 系统设置
  - 日志级别配置
  - 调试模式
  - 历史记录管理

## 安装说明

### 后端安装

1. 创建Python虚拟环境：
```bash
python -m venv .venv
```

2. 激活虚拟环境：
```bash
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

### 前端安装

1. 进入web目录：
```bash
cd web
```

2. 安装依赖：
```bash
npm install
```

## 运行说明

### 启动后端

```bash
python main.py
```

后端服务将在 http://localhost:8000 启动。

### 启动前端

```bash
cd web
npm run dev
```

前端开发服务器将在 http://localhost:5173 启动。

## API文档

启动后端服务后，可以访问 http://localhost:8000/docs 查看完整的API文档。

### 主要API端点

- `/api/system-info`：获取系统信息
- `/api/directory-info`：获取目录信息
- `/api/test-server-connection`：测试服务器连接
- `/api/test-ai-config`：测试AI配置
- `/api/save-config`：保存系统配置
- `/api/get-config`：获取系统配置

## 配置说明

配置文件位于项目根目录的 `config.yaml`，包含以下主要配置项：

- general：通用配置
  - web_server：Web服务器配置
  - debug_mode：调试模式
  - history_size：历史记录大小
- ai：AI相关配置
  - provider：AI提供商
  - model：模型配置
  - api_key：API密钥
- security：安全配置
  - dangerous_commands：危险命令列表
  - require_confirmation：操作确认
- logging：日志配置
  - level：日志级别
  - file：日志文件

## 开发指南

### 添加新的API端点

1. 在 `ata/api/` 目录下创建新的API模块
2. 在 `main.py` 中注册新的路由
3. 更新API文档

### 添加新的前端组件

1. 在 `web/src/components/` 目录下创建新组件
2. 在 `App.vue` 中引入并使用组件
3. 更新相关文档

## 常见问题

1. 启动失败
   - 检查端口是否被占用
   - 确认所有依赖已正确安装
   - 检查配置文件格式

2. 连接测试失败
   - 确认服务器地址和端口正确
   - 检查网络连接
   - 查看错误日志

3. AI配置问题
   - 确认API密钥正确
   - 检查选择的模型是否可用
   - 确认网络可以访问AI服务

## 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License 