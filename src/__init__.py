"""
Taxi Service - 出租车服务系统
A Flask-based REST API for managing taxi bookings, drivers, and rides.
"""

__version__ = '1.0.0'
__author__ = 'Your Name'
__email__ = 'your.email@example.com'

# 导入主要的类和函数，方便直接导入
# 注意：我们不再有 create_app 函数，只有一个 app 实例
from .app import app

# 包级别的日志配置
import logging

# 设置默认的日志格式
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 创建包级别的日志器
logger = logging.getLogger(__name__)

# 可以在这里定义一些包级别的异常
class TaxiServiceError(Exception):
    """出租车服务的基础异常类"""
    pass

class AuthenticationError(TaxiServiceError):
    """认证异常"""
    pass

class ValidationError(TaxiServiceError):
    """数据验证异常"""
    pass

class DatabaseError(TaxiServiceError):
    """数据库操作异常"""
    pass

class PaymentError(TaxiServiceError):
    """支付异常"""
    pass

# 导出常用的类和函数
__all__ = [
    'app',  # 只导出 app，不导出 create_app
    'TaxiServiceError',
    'AuthenticationError',
    'ValidationError',
    'DatabaseError',
    'PaymentError',
    'logger'
]