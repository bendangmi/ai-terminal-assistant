"""
配置管理器测试模块
"""

import os
import json
import yaml
import pytest
from pathlib import Path
from typing import Dict, Any

from ata.config_manager import ConfigManager, ConfigValidationError


@pytest.fixture
def temp_config_dir(tmp_path: Path) -> Path:
    """创建临时配置目录"""
    config_dir = tmp_path / ".ata"
    config_dir.mkdir()
    return config_dir


@pytest.fixture
def config_manager(temp_config_dir: Path) -> ConfigManager:
    """创建配置管理器实例"""
    config_path = temp_config_dir / "config.yaml"
    return ConfigManager(str(config_path))


def test_default_config(config_manager: ConfigManager) -> None:
    """测试默认配置"""
    assert config_manager.config["version"] == ConfigManager.CONFIG_SCHEMA["version"]
    assert "general" in config_manager.config
    assert "ai" in config_manager.config
    assert "security" in config_manager.config
    assert "ui" in config_manager.config
    assert "logging" in config_manager.config


def test_get_config_value(config_manager: ConfigManager) -> None:
    """测试获取配置值"""
    # 测试获取存在的值
    assert config_manager.get("general.history_size") == 20
    assert config_manager.get("ai.provider") == "openai"
    
    # 测试获取不存在的值
    assert config_manager.get("not.exist", "default") == "default"
    assert config_manager.get("not.exist") is None


def test_set_config_value(config_manager: ConfigManager) -> None:
    """测试设置配置值"""
    # 设置已存在的值
    config_manager.set("general.history_size", 30)
    assert config_manager.get("general.history_size") == 30
    
    # 设置新值
    config_manager.set("custom.key", "value")
    assert config_manager.get("custom.key") == "value"


def test_config_validation(config_manager: ConfigManager) -> None:
    """测试配置验证"""
    # 测试有效值
    config_manager.set("general.history_size", 50, validate=True)
    assert config_manager.get("general.history_size") == 50
    
    # 测试无效值
    with pytest.raises(ValueError):
        config_manager.set("general.history_size", "invalid", validate=True)
    
    # 验证配置未被修改
    assert config_manager.get("general.history_size") == 50


def test_config_backup(temp_config_dir: Path, config_manager: ConfigManager) -> None:
    """测试配置备份"""
    # 修改配置并保存
    config_manager.set("general.history_size", 40)
    config_manager.save_config()
    
    # 检查备份文件
    backups = list((temp_config_dir / "backups").glob("config_*.yaml"))
    assert len(backups) > 0


def test_export_import_config(temp_config_dir: Path, config_manager: ConfigManager) -> None:
    """测试配置导出和导入"""
    # 修改配置
    config_manager.set("general.history_size", 60)
    
    # 导出配置
    export_path = temp_config_dir / "exported_config.yaml"
    assert config_manager.export_config(export_path)
    
    # 重置配置
    config_manager.reset_to_defaults()
    assert config_manager.get("general.history_size") == 20
    
    # 导入配置
    assert config_manager.import_config(export_path)
    assert config_manager.get("general.history_size") == 60


def test_config_schema_validation(config_manager: ConfigManager) -> None:
    """测试配置模式验证"""
    errors = config_manager.validate_config()
    assert len(errors) == 0
    
    # 添加无效值
    config_manager.config["general"]["history_size"] = "invalid"
    errors = config_manager.validate_config()
    assert len(errors) > 0
    assert any(e.path == "general.history_size" for e in errors)


def test_provider_config(config_manager: ConfigManager) -> None:
    """测试提供商配置"""
    # 测试获取当前提供商配置
    provider_config = config_manager.get_provider_config()
    assert "model" in provider_config
    assert "temperature" in provider_config
    assert "api_key_env" in provider_config
    
    # 测试获取指定提供商配置
    deepseek_config = config_manager.get_provider_config("deepseek")
    assert deepseek_config["model"] == "deepseek-chat"


def test_available_providers(config_manager: ConfigManager) -> None:
    """测试可用提供商列表"""
    providers = config_manager.get_available_providers()
    assert "openai" in providers
    assert "deepseek" in providers


def test_model_selection(config_manager: ConfigManager) -> None:
    """测试模型选择"""
    # 测试OpenAI模型
    openai_model = config_manager.get_model_for_provider("openai")
    assert openai_model in ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"]
    
    # 测试DeepSeek模型
    deepseek_model = config_manager.get_model_for_provider("deepseek")
    assert deepseek_model in ["deepseek-chat", "deepseek-coder"]


def test_api_key_env(config_manager: ConfigManager) -> None:
    """测试API密钥环境变量"""
    # 测试OpenAI API密钥环境变量
    openai_key_env = config_manager.get_api_key_env_for_provider("openai")
    assert openai_key_env == "OPENAI_API_KEY"
    
    # 测试DeepSeek API密钥环境变量
    deepseek_key_env = config_manager.get_api_key_env_for_provider("deepseek")
    assert deepseek_key_env == "DEEPSEEK_API_KEY"


def test_config_file_encoding(temp_config_dir: Path, config_manager: ConfigManager) -> None:
    """测试配置文件编码"""
    # 设置包含中文的值
    config_manager.set("custom.chinese", "你好世界")
    config_manager.save_config()
    
    # 重新加载配置
    new_config = ConfigManager(str(temp_config_dir / "config.yaml"))
    assert new_config.get("custom.chinese") == "你好世界"


def test_config_merge(temp_config_dir: Path) -> None:
    """测试配置合并"""
    # 创建自定义配置文件
    config_path = temp_config_dir / "config.yaml"
    custom_config = {
        "version": ConfigManager.CONFIG_SCHEMA["version"],
        "general": {
            "history_size": 100,
            "custom_setting": "value"
        }
    }
    
    with open(config_path, "w", encoding="utf-8") as f:
        yaml.dump(custom_config, f)
    
    # 加载配置
    config_manager = ConfigManager(str(config_path))
    
    # 验证合并结果
    assert config_manager.get("general.history_size") == 100
    assert config_manager.get("general.custom_setting") == "value"
    assert config_manager.get("ai.provider") == "openai"  # 默认值


def test_config_migration(temp_config_dir: Path) -> None:
    """测试配置迁移"""
    # 创建旧版本配置文件
    config_path = temp_config_dir / "config.yaml"
    old_config = {
        "version": "0.9.0",
        "general": {
            "history_size": 10
        }
    }
    
    with open(config_path, "w", encoding="utf-8") as f:
        yaml.dump(old_config, f)
    
    # 加载配置（会触发迁移）
    config_manager = ConfigManager(str(config_path))
    
    # 验证迁移结果
    assert config_manager.config["version"] == ConfigManager.CONFIG_SCHEMA["version"]
    assert config_manager.get("general.history_size") == 10


def test_invalid_config_recovery(temp_config_dir: Path) -> None:
    """测试无效配置恢复"""
    # 创建无效的配置文件
    config_path = temp_config_dir / "config.yaml"
    with open(config_path, "w") as f:
        f.write("invalid: yaml: content")
    
    # 加载配置（应该使用默认值）
    config_manager = ConfigManager(str(config_path))
    
    # 验证是否使用了默认配置
    assert config_manager.get("general.history_size") == 20
    assert config_manager.get("ai.provider") == "openai" 