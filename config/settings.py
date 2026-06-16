# -*- coding: utf-8 -*-
"""
AutoTest Hub 配置管理模块
@Function: 加载和管理应用配置，支持环境变量和配置文件
"""

import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 项目根目录
BASE_DIR = Path(__file__).parent.parent


class DatabaseSettings(BaseSettings):
    """数据库配置"""
    url: str = Field(default="sqlite:///./data/autotest.db", alias="DATABASE_URL")
    
    class Config:
        env_prefix = ""


class ServerSettings(BaseSettings):
    """服务器配置"""
    backend_port: int = Field(default=8000, alias="BACKEND_PORT")
    frontend_port: int = Field(default=5173, alias="FRONTEND_PORT")
    debug: bool = Field(default=True, alias="DEBUG")
    host: str = "127.0.0.1"
    
    class Config:
        env_prefix = ""


class AISettings(BaseSettings):
    """AI 诊断配置"""
    api_key: Optional[str] = Field(default=None, alias="OPENAI_API_KEY")
    api_base: str = Field(default="https://api.openai.com/v1", alias="OPENAI_API_BASE")
    model: str = Field(default="gpt-4", alias="OPENAI_MODEL")
    
    class Config:
        env_prefix = ""


class NotificationSettings(BaseSettings):
    """通知配置"""
    smtp_host: Optional[str] = Field(default=None, alias="SMTP_HOST")
    smtp_port: int = Field(default=587, alias="SMTP_PORT")
    smtp_user: Optional[str] = Field(default=None, alias="SMTP_USER")
    smtp_password: Optional[str] = Field(default=None, alias="SMTP_PASSWORD")
    smtp_from: Optional[str] = Field(default=None, alias="SMTP_FROM")
    dingtalk_webhook: Optional[str] = Field(default=None, alias="DINGTALK_WEBHOOK")
    wechat_webhook: Optional[str] = Field(default=None, alias="WECHAT_WEBHOOK")
    
    class Config:
        env_prefix = ""


class ExecutionSettings(BaseSettings):
    """执行配置"""
    default_timeout: int = Field(default=30, alias="DEFAULT_TIMEOUT")
    screenshot_path: str = Field(default="./data/screenshots", alias="SCREENSHOT_PATH")
    video_path: str = Field(default="./data/videos", alias="VIDEO_PATH")
    log_path: str = Field(default="./logs", alias="LOG_PATH")
    
    class Config:
        env_prefix = ""


class Settings(BaseSettings):
    """应用主配置"""
    # 服务配置
    server: ServerSettings = ServerSettings()
    database: DatabaseSettings = DatabaseSettings()
    ai: AISettings = AISettings()
    notification: NotificationSettings = NotificationSettings()
    execution: ExecutionSettings = ExecutionSettings()
    
    # 路径配置
    base_dir: Path = BASE_DIR
    data_dir: Path = BASE_DIR / "data"
    log_dir: Path = BASE_DIR / "logs"
    
    def ensure_dirs(self):
        """确保必要目录存在"""
        dirs = [
            self.data_dir,
            self.log_dir,
            Path(self.execution.screenshot_path),
            Path(self.execution.video_path),
        ]
        for d in dirs:
            if not d.is_absolute():
                d = self.base_dir / d
            d.mkdir(parents=True, exist_ok=True)


# 全局配置实例
settings = Settings()


def get_settings() -> Settings:
    """获取配置实例"""
    return settings
