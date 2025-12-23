"""
服务模块 - 包含业务逻辑和外部服务集成
"""

# 导入所有服务
from .database import db
from .location import LocationService
from .notification import NotificationService
from .payment import PaymentService  # 现在有这个模块了

# 导出所有服务
__all__ = [
    'db',
    'LocationService',
    'NotificationService',
    'PaymentService'
]

# 服务初始化函数
def init_services(app):
    """初始化所有服务"""
    # 初始化数据库
    db.init_app(app)

    # 创建数据库表（如果不存在）
    with app.app_context():
        db.create_all()

    return True

# 服务健康检查
def check_services_health():
    """检查所有服务的健康状态"""
    health_status = {}

    # 检查数据库
    try:
        from .database import db
        db.session.execute('SELECT 1')
        health_status['database'] = {'status': 'healthy', 'message': 'OK'}
    except Exception as e:
        health_status['database'] = {'status': 'unhealthy', 'message': str(e)}

    # 在这里添加其他服务的健康检查
    # 例如：Redis、外部API等

    # 总体状态
    all_healthy = all(status['status'] == 'healthy' for status in health_status.values())
    health_status['overall'] = 'healthy' if all_healthy else 'unhealthy'

    return health_status