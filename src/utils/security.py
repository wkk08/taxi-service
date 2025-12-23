"""
安全工具模块 - 处理密码哈希、JWT令牌等安全相关功能
"""
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask import request, jsonify


class SecurityUtils:
    """安全工具类"""

    @staticmethod
    def hash_password(password: str) -> str:
        """哈希密码

        Args:
            password: 明文密码

        Returns:
            哈希后的密码
        """
        return generate_password_hash(password)

    @staticmethod
    def verify_password(hashed_password: str, password: str) -> bool:
        """验证密码

        Args:
            hashed_password: 哈希密码
            password: 明文密码

        Returns:
            是否匹配
        """
        return check_password_hash(hashed_password, password)

    @staticmethod
    def generate_token(user_id: int, email: str, role: str, secret_key: str, expires_hours: int = 24) -> str:
        """生成JWT令牌

        Args:
            user_id: 用户ID
            email: 用户邮箱
            role: 用户角色
            secret_key: 密钥
            expires_hours: 过期时间（小时）

        Returns:
            JWT令牌字符串
        """
        payload = {
            'user_id': user_id,
            'email': email,
            'role': role,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=expires_hours),
            'iat': datetime.datetime.utcnow()
        }

        return jwt.encode(payload, secret_key, algorithm='HS256')

    @staticmethod
    def verify_token(token: str, secret_key: str):
        """验证JWT令牌

        Args:
            token: JWT令牌
            secret_key: 密钥

        Returns:
            解码后的payload或None（如果无效）
        """
        try:
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None  # 令牌过期
        except jwt.InvalidTokenError:
            return None  # 无效令牌

    @staticmethod
    def sanitize_input(input_string: str) -> str:
        """清理用户输入，防止XSS攻击

        Args:
            input_string: 用户输入字符串

        Returns:
            清理后的字符串
        """
        import html
        if not input_string:
            return ""

        # 移除HTML标签
        import re
        cleaned = re.sub(r'<[^>]*>', '', str(input_string))

        # HTML转义
        escaped = html.escape(cleaned)

        # 移除额外的空白字符
        return escaped.strip()

    @staticmethod
    def validate_email(email: str) -> bool:
        """验证邮箱格式

        Args:
            email: 邮箱地址

        Returns:
            是否有效
        """
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    @staticmethod
    def validate_phone(phone: str) -> bool:
        """验证电话号码格式

        Args:
            phone: 电话号码

        Returns:
            是否有效
        """
        import re
        # 简单的手机号验证（支持国际格式）
        pattern = r'^\+?[1-9]\d{1,14}$'  # E.164格式
        return bool(re.match(pattern, phone))

    @staticmethod
    def validate_password(password: str) -> tuple[bool, str]:
        """验证密码强度

        Args:
            password: 密码

        Returns:
            (是否有效, 错误信息)
        """
        if len(password) < 8:
            return False, "密码必须至少8个字符"

        if len(password) > 128:
            return False, "密码不能超过128个字符"

        # 检查是否包含数字
        if not any(char.isdigit() for char in password):
            return False, "密码必须包含至少一个数字"

        # 检查是否包含字母
        if not any(char.isalpha() for char in password):
            return False, "密码必须包含至少一个字母"

        # 可选：检查特殊字符
        # import string
        # if not any(char in string.punctuation for char in password):
        #     return False, "密码必须包含至少一个特殊字符"

        return True, "密码有效"


def token_required(f):
    """JWT令牌验证装饰器

    Args:
        f: 被装饰的函数

    Returns:
        装饰后的函数
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # 从请求头获取令牌
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

        if not token:
            return jsonify({
                'success': False,
                'message': 'Token is missing'
            }), 401

        try:
            # 这里需要SECRET_KEY，暂时使用默认值
            # 实际项目中应该从配置中获取
            secret_key = 'your-secret-key-change-me'
            data = SecurityUtils.verify_token(token, secret_key)

            if data is None:
                return jsonify({
                    'success': False,
                    'message': 'Invalid or expired token'
                }), 401

            # 将用户信息添加到kwargs中，供路由函数使用
            kwargs['user_id'] = data.get('user_id')
            kwargs['user_email'] = data.get('email')
            kwargs['user_role'] = data.get('role')

        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Token validation failed: {str(e)}'
            }), 401

        return f(*args, **kwargs)

    return decorated


def role_required(required_role):
    """角色验证装饰器

    Args:
        required_role: 所需的角色（如 'admin', 'driver', 'passenger'）

    Returns:
        装饰后的函数
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 首先确保有token验证
            if 'user_role' not in kwargs:
                return jsonify({
                    'success': False,
                    'message': 'Authentication required'
                }), 401

            # 检查角色权限
            user_role = kwargs.get('user_role')
            if user_role != required_role:
                return jsonify({
                    'success': False,
                    'message': f'Insufficient permissions. Required role: {required_role}',
                    'your_role': user_role
                }), 403

            return f(*args, **kwargs)
        return decorated_function
    return decorator


# 创建工具实例
security = SecurityUtils()

# 导出常用函数
hash_password = security.hash_password
verify_password = security.verify_password
generate_token = security.generate_token
verify_token = security.verify_token
sanitize_input = security.sanitize_input
validate_email = security.validate_email
validate_phone = security.validate_phone
validate_password = security.validate_password

# 导出类
__all__ = [
    'SecurityUtils',
    'security',
    'hash_password',
    'verify_password',
    'generate_token',
    'verify_token',
    'sanitize_input',
    'validate_email',
    'validate_phone',
    'validate_password',
    'token_required',
    'role_required'
]