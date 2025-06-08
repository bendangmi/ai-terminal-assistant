# DeepSeek模型研究报告

## 1. DeepSeek模型概述

DeepSeek提供了两种主要的大型语言模型：

1. **DeepSeek-V3-0324**（通过`deepseek-chat`访问）
   - 一个通用的聊天模型
   - 具有强大的推理性能
   - 增强的前端开发技能
   - 智能的工具使用能力
   - 适合非复杂推理任务

2. **DeepSeek-R1-0528**（通过`deepseek-reasoner`访问）
   - 专门用于复杂推理任务的模型
   - 改进的基准性能
   - 增强的前端能力
   - 减少幻觉
   - 支持JSON输出和函数调用

## 2. API兼容性

DeepSeek API使用与OpenAI兼容的API格式，这意味着：

- 可以通过修改配置来使用OpenAI SDK或与OpenAI API兼容的软件访问DeepSeek API
- 基本URL：`https://api.deepseek.com`（也可以使用`https://api.deepseek.com/v1`以保持与OpenAI完全兼容）
- 需要申请DeepSeek API密钥

## 3. Python示例代码

```python
from openai import OpenAI

client = OpenAI(api_key="<DeepSeek API Key>", base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-chat",  # 或 "deepseek-reasoner" 用于复杂推理任务
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"}
    ],
    stream=False
)

print(response.choices[0].message.content)
```

## 4. 定价信息

DeepSeek的定价基于每百万（1M）令牌，分为输入和输出令牌：

### DeepSeek-chat (V3-0324)
- 输入令牌（缓存命中）：$0.07/1M
- 输入令牌（缓存未命中）：$0.27/1M
- 输出令牌：$1.10/1M

### DeepSeek-reasoner (R1-0528)
- 输入令牌（缓存命中）：$0.14/1M
- 输入令牌（缓存未命中）：$0.55/1M
- 输出令牌：$2.19/1M

DeepSeek还提供非高峰时段（UTC 16:30-00:30）的折扣价格。

## 5. 模型特点

### 上下文长度
- DeepSeek-chat：64K
- DeepSeek-reasoner：64K

### 最大输出
- DeepSeek-chat：默认4K，最大8K
- DeepSeek-reasoner：默认32K，最大64K

### 功能支持
两种模型都支持：
- JSON输出
- 函数调用
- 聊天前缀补全（测试版）

DeepSeek-chat还支持FIM补全（测试版）。

## 6. 许可证信息

两种模型都在MIT许可证下发布，开源权重可在Hugging Face上获取：
- DeepSeek-V3-0324：https://huggingface.co/deepseek-ai/DeepSeek-V3-0324
- DeepSeek-R1-0528：https://huggingface.co/deepseek-ai/DeepSeek-R1-0528

## 7. 与OpenAI相比的优势

1. **开源**：DeepSeek模型是开源的，可以在本地部署
2. **价格**：相比OpenAI，DeepSeek的价格更具竞争力
3. **长上下文**：两种模型都支持64K的上下文长度
4. **API兼容性**：与OpenAI API兼容，便于迁移
5. **专业化模型**：提供专门用于推理的模型（DeepSeek-R1）

## 8. 集成建议

对于AI终端助手项目，建议：
1. 保留OpenAI作为默认选项
2. 添加DeepSeek作为替代选项
3. 对于复杂的命令生成和推理任务，使用DeepSeek-reasoner
4. 对于简单的对话和命令生成，使用DeepSeek-chat
5. 允许用户在配置中选择首选的AI提供商

