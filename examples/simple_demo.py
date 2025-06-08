#!/usr/bin/env python3
"""
AI终端助手示例脚本

这个脚本演示了如何使用AI终端助手的核心功能。
"""

import os
import sys
import asyncio
import platform
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from ata.ai_interface import AIInterface
from ata.command_executor import CommandExecutor
from ata.config_manager import ConfigManager


async def main():
    """主函数"""
    # 检查API密钥
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("错误: 未设置OPENAI_API_KEY环境变量")
        print("请设置环境变量: export OPENAI_API_KEY='your-api-key'")
        return 1

    # 创建配置管理器
    config_manager = ConfigManager()

    # 创建AI接口
    ai_interface = AIInterface(config_manager)

    # 创建命令执行器
    command_executor = CommandExecutor(config_manager)

    # 用户输入
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
    else:
        print("请输入您想要执行的操作（用自然语言描述）:")
        user_input = input("> ")

    print(f"\n正在处理: {user_input}")
    print("思考中...\n")

    try:
        # 生成命令
        response = await ai_interface.chat(user_input)

        # 显示生成的命令
        print("生成的命令:")
        print(f"  {response}")
        print()

        # 检查命令是否危险
        is_dangerous, warnings = command_executor.is_dangerous(response)
        if is_dangerous:
            print("安全警告:")
            for warning in warnings:
                print(f"  - {warning}")
            print()

        # 获取用户确认
        while True:
            choice = input("是否执行此命令? (y/n/e - 执行/取消/编辑): ").lower()

            if choice == "y":
                # 执行命令
                print("\n执行命令...")
                result = command_executor.execute(response)

                # 显示结果
                print("\n执行结果:")
                if result.success:
                    print("  命令执行成功")
                else:
                    print("  命令执行失败")

                if result.stdout:
                    print("\n输出:")
                    print(result.stdout)

                if result.stderr:
                    print("\n错误:")
                    print(result.stderr)

                print(f"\n退出代码: {result.exit_code}")
                break

            elif choice == "e":
                # 编辑命令
                print("\n原始命令:")
                print(f"  {response}")
                edited_command = input("编辑命令: ")

                if edited_command:
                    print("\n执行命令...")
                    result = command_executor.execute(edited_command)

                    # 显示结果
                    print("\n执行结果:")
                    if result.success:
                        print("  命令执行成功")
                    else:
                        print("  命令执行失败")

                    if result.stdout:
                        print("\n输出:")
                        print(result.stdout)

                    if result.stderr:
                        print("\n错误:")
                        print(result.stderr)

                    print(f"\n退出代码: {result.exit_code}")
                break

            elif choice == "n":
                print("已取消执行")
                break

            else:
                print("无效的选择，请重新输入")

    except Exception as e:
        print(f"错误: {str(e)}")
        return 1

    return 0


if __name__ == "__main__":
    try:
        sys.exit(asyncio.run(main()))
    except KeyboardInterrupt:
        print("\n程序已中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n发生错误: {str(e)}")
        sys.exit(1)

