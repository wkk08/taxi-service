"""
数据库服务 - 数据库连接和初始化
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# 创建SQLAlchemy实例
db = SQLAlchemy()

# 创建迁移实例
migrate = Migrate()


def init_database(app):
    """初始化数据库连接"""
    db.init_app(app)
    migrate.init_app(app, db)

    # 可选：创建数据库表（如果不存在）
    with app.app_context():
        db.create_all()

    return db