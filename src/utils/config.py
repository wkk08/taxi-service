"""
配置管理工具
"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class Config:
    """基础配置类"""
    # Flask配置
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///taxi.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT配置
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 24))  # 小时

    # Redis配置
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')

    # 应用配置
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    SQLALCHEMY_ECHO = True  # 输出SQL语句


class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):
    """生产环境配置"""
    # 生产环境应该从环境变量获取所有敏感信息
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')

    # 禁用调试模式
    DEBUG = False

    # 生产数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    # 添加生产环境特定的配置
    # 例如：日志级别、性能配置等