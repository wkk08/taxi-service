"""
API模块 - 包含所有REST API端点的蓝图层
"""

# 导入所有蓝图，方便在app.py中统一注册
from .auth import auth_bp
from .booking import booking_bp
from .driver import driver_bp
from .notification import notification_bp

# 导出所有蓝图
__all__ = [
    'auth_bp',
    'booking_bp',
    'driver_bp',
    'notification_bp'
]

# API版本信息
API_VERSION = 'v1'
API_PREFIX = f'/api/{API_VERSION}'

# 可以在这里定义API相关的常量
# HTTP状态码常量
HTTP_OK = 200
HTTP_CREATED = 201
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401
HTTP_FORBIDDEN = 403
HTTP_NOT_FOUND = 404
HTTP_INTERNAL_ERROR = 500

# API响应格式
def api_response(success=True, message="", data=None, code=HTTP_OK):
    """标准化的API响应格式"""
    return {
        'success': success,
        'message': message,
        'data': data,
        'code': code
    }, code

def error_response(message="An error occurred", code=HTTP_BAD_REQUEST):
    """错误响应格式"""
    return api_response(False, message, None, code)