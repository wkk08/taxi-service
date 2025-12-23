"""
测试配置 - 修复Flask 2.3+兼容性问题
"""
import pytest
from flask import Flask
from src.services.database import db

@pytest.fixture
def app():
    """创建测试应用"""
    app = Flask(__name__)
    app.config.update({
        'TESTING': True,
        'SECRET_KEY': 'test-secret-key',
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })

    db.init_app(app)

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    """测试客户端"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """CLI运行器"""
    return app.test_cli_runner()