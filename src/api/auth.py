"""
认证API - 用户注册和登录
"""
from flask import Blueprint, request, jsonify
from src.utils.security import hash_password, verify_password, generate_token

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    try:
        data = request.get_json()

        # 简化注册逻辑
        return jsonify({
            "success": True,
            "message": "注册功能待实现",
            "data": {
                "email": data.get('email', '未提供')
            }
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"注册失败: {str(e)}"
        }), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    try:
        data = request.get_json()

        # 简化登录逻辑
        return jsonify({
            "success": True,
            "message": "登录功能待实现",
            "token": "dummy-token-placeholder"
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"登录失败: {str(e)}"
        }), 500


@auth_bp.route('/test', methods=['GET'])
def test():
    """测试端点"""
    return jsonify({
        "success": True,
        "message": "Auth API is working!"
    })