"""
工具模块 - 包含辅助函数、配置和工具类
"""

# 导入所有工具
from .config import Config, DevelopmentConfig, ProductionConfig, TestingConfig
from .security import (
    hash_password,
    verify_password,
    generate_token,
    verify_token,
    validate_email,
    validate_phone,
    validate_password
)
from .validators import (
    validate_coordinates,
    validate_username,
    validate_address,
    validate_fare,
    validate_rating
)

# 工具函数
def format_response_time(start_time, end_time):
    """计算并格式化响应时间"""
    import time
    elapsed = end_time - start_time
    return {
        'seconds': elapsed,
        'milliseconds': elapsed * 1000,
        'formatted': f"{elapsed:.4f} seconds"
    }

def setup_logging(level='INFO'):
    """设置应用程序的日志配置"""
    import logging

    log_level = getattr(logging, level.upper(), logging.INFO)

    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    return logging.getLogger(__name__)

# 导出所有工具
__all__ = [
    'Config',
    'DevelopmentConfig',
    'ProductionConfig',
    'TestingConfig',
    'hash_password',
    'verify_password',
    'generate_token',
    'verify_token',
    'validate_email',
    'validate_phone',
    'validate_password',
    'validate_coordinates',
    'validate_username',
    'validate_address',
    'validate_fare',
    'validate_rating',
    'format_response_time',
    'setup_logging'
]