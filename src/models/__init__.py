"""
数据模型模块 - 包含所有数据库模型类
"""

# 导入所有模型类，方便在其他地方导入
from .user import User
from .ride import Ride
from .vehicle import Vehicle

# 导出所有模型类
__all__ = [
    'User',
    'Ride',
    'Vehicle'
]

# 数据库配置相关
from src.services.database import db

# 创建所有表的函数
def create_tables():
    """创建所有数据库表"""
    db.create_all()
    return True

# 删除所有表的函数（仅用于测试）
def drop_tables():
    """删除所有数据库表"""
    db.drop_all()
    return True

# 数据库连接状态检查
def check_database_connection():
    """检查数据库连接状态"""
    try:
        # 尝试执行一个简单的查询
        db.session.execute('SELECT 1')
        return True, "Database connection successful"
    except Exception as e:
        return False, f"Database connection failed: {str(e)}"

# 模型关系的导入
# 这里可以导入一些常用的查询或关系
from sqlalchemy.orm import relationship, backref