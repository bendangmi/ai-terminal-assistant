"""
AI Terminal Assistant (ATA) 的安装配置
"""

from setuptools import setup, find_packages
import os

# 读取README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# 读取依赖
def read_requirements(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        return []

setup(
    name="ata",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "openai>=1.0.0",
        "rich>=10.0.0",
        "pyyaml>=6.0.0",
        "requests>=2.0.0",
        "pydantic>=2.0.0",
        "typing-extensions>=4.0.0",
        "python-dotenv>=1.0.0",
        "quart>=0.18.4",
        "quart-cors>=0.7.0",
        "psutil>=5.9.0"
    ],
    python_requires=">=3.8",
    author="Your Name",
    author_email="your.email@example.com",
    description="AI Terminal Assistant",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ai-terminal-assistant",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "ata=ata.__main__:main",
        ],
    },
    keywords="ai, terminal, assistant, cli, automation",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/ai-terminal-assistant/issues",
        "Source": "https://github.com/yourusername/ai-terminal-assistant",
        "Documentation": "https://github.com/yourusername/ai-terminal-assistant/docs",
    },
)

