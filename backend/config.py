"""
配置管理模块
使用 Pydantic Settings 管理环境变量
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """应用配置类"""
    
    # 数据库配置
    # 请修改密码为你的 MySQL root 密码
    DATABASE_URL: str = "mysql+pymysql://root:151362@localhost:3306/online_mall"
    
    # JWT配置
    JWT_SECRET_KEY: str = "JWT_SECRET_KEY=K9mP2xL7vN4qR8wE6tY3uI1oA5sD0fG9hJ2kZ8xC7vB6nM4lQ3wE"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24小时
    
    # 应用配置
    APP_NAME: str = "网上商城系统"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # CORS配置
    CORS_ORIGINS: list = ["http://localhost:5173", "http://localhost:3000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# 创建全局配置实例
settings = Settings()
