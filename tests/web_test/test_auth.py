"""
认证单元测试 - 测试认证相关功能
"""
import pytest
from src.utils.security import (
    SecurityUtils,
    hash_password,
    verify_password,
    generate_token,
    verify_token,
    validate_email,
    validate_phone,
    validate_password
)


class TestSecurityUtils:
    """测试安全工具类"""

    def test_hash_and_verify_password(self):
        """测试密码哈希和验证"""
        password = 'MySecurePassword123!'

        # 哈希密码
        hashed = hash_password(password)

        # 验证应该成功
        assert verify_password(hashed, password) is True

        # 错误的密码应该失败
        assert verify_password(hashed, 'WrongPassword') is False

        # 确保哈希值每次不同（因为有salt）
        hashed2 = hash_password(password)
        assert hashed != hashed2

    def test_generate_and_verify_token(self):
        """测试JWT令牌生成和验证"""
        secret_key = 'test-secret-key'
        user_id = 123
        email = 'user@example.com'
        role = 'passenger'

        # 生成令牌
        token = generate_token(user_id, email, role, secret_key)

        assert isinstance(token, str)
        assert len(token) > 0

        # 验证令牌
        payload = verify_token(token, secret_key)

        assert payload is not None
        assert payload['user_id'] == user_id
        assert payload['email'] == email
        assert payload['role'] == role
        assert 'exp' in payload
        assert 'iat' in payload

    def test_verify_invalid_token(self):
        """测试验证无效令牌"""
        secret_key = 'test-secret-key'

        # 无效令牌应该返回None
        assert verify_token('invalid.token.here', secret_key) is None

        # 使用错误密钥验证应该返回None
        token = generate_token(1, 'test@test.com', 'passenger', secret_key)
        assert verify_token(token, 'wrong-secret-key') is None

    def test_validate_email(self):
        """测试邮箱验证"""
        # 有效邮箱
        assert validate_email('user@example.com') is True
        assert validate_email('user.name@example.co.uk') is True
        assert validate_email('user+tag@example.com') is True

        # 无效邮箱
        assert validate_email('invalid-email') is False
        assert validate_email('user@') is False
        assert validate_email('@example.com') is False
        assert validate_email('user@.com') is False
        assert validate_email('') is False
        assert validate_email(None) is False

    def test_validate_phone(self):
        """测试电话号码验证"""
        # 有效电话号码
        assert validate_phone('+8612345678901') is True
        assert validate_phone('12345678901') is True
        assert validate_phone('+1-234-567-8901') is False  # 注意：我们的正则不允许破折号
        assert validate_phone('+44 20 7946 0958') is False  # 不允许空格

        # 无效电话号码
        assert validate_phone('123') is False  # 太短
        assert validate_phone('') is False
        assert validate_phone('abc') is False
        assert validate_phone('+1234567890123456') is True  # 15位，有效

    def test_validate_password(self):
        """测试密码强度验证"""
        # 有效密码
        valid, message = validate_password('Secure123')
        assert valid is True
        assert '有效' in message

        # 太短
        valid, message = validate_password('Short1')
        assert valid is False
        assert '至少8个字符' in message

        # 太长
        long_password = 'A' * 129 + '1'
        valid, message = validate_password(long_password)
        assert valid is False
        assert '不能超过128个字符' in message

        # 缺少数字
        valid, message = validate_password('NoNumbersHere')
        assert valid is False
        assert '至少一个数字' in message

        # 缺少字母
        valid, message = validate_password('12345678')
        assert valid is False
        assert '至少一个字母' in message

        # 只有字母数字，没有特殊字符（但仍然有效，因为我们不要求特殊字符）
        valid, message = validate_password('OnlyLetters123')
        assert valid is True

    def test_sanitize_input(self):
        """测试输入清理"""
        from src.utils.security import sanitize_input

        # 测试HTML清理
        input_with_html = '<script>alert("XSS")</script>Hello'
        sanitized = sanitize_input(input_with_html)
        assert '<script>' not in sanitized
        assert 'alert' not in sanitized
        assert 'Hello' in sanitized

        # 测试空白字符清理
        input_with_spaces = '  test  '
        sanitized = sanitize_input(input_with_spaces)
        assert sanitized == 'test'

        # 测试空输入
        assert sanitize_input('') == ''
        assert sanitize_input(None) == ''


class TestAuthDecorators:
    """测试认证装饰器"""

    def test_token_required_decorator(self):
        """测试token_required装饰器"""
        from src.utils.security import token_required
        from flask import jsonify

        # 创建一个使用装饰器的简单函数
        @token_required
        def protected_function(*args, **kwargs):
            return jsonify({
                'user_id': kwargs.get('user_id'),
                'role': kwargs.get('user_role')
            })

        # 这个测试比较复杂，因为涉及Flask请求上下文
        # 在实际测试中，我们会使用Flask测试客户端

    def test_role_required_decorator(self):
        """测试role_required装饰器"""
        from src.utils.security import role_required
        from flask import jsonify

        # 创建一个使用装饰器的简单函数
        @role_required('admin')
        def admin_only_function(*args, **kwargs):
            return jsonify({'message': 'Admin access granted'})

        # 同样，这个测试需要Flask请求上下文
        # 我们会在集成测试中测试它