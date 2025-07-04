# 变更日志

本文档记录AI终端助手（ATA）的所有重要变更。

格式基于[Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
并且本项目遵循[语义化版本](https://semver.org/lang/zh-CN/)。

## [未发布]

### 新增

- 添加对Azure OpenAI的支持
- 添加命令历史功能
- 添加彩色输出选项

### 修复

- 修复Windows上的路径问题
- 修复超时处理逻辑

### 变更

- 改进错误消息
- 优化提示模板

## [0.1.0] - 2025-06-07

### 新增

- 初始版本发布
- 支持通过自然语言生成命令
- 提供命令解释和安全警告
- 实现命令确认机制
- 支持命令编辑
- 添加交互模式
- 支持Linux和macOS平台
- 添加基本的Windows支持（实验性）
- 提供详细的文档和示例

### 安全

- 实现危险命令检测
- 添加权限提升警告
- 实现命令执行超时机制

