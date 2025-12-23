"""
车辆模型 - 存储司机车辆信息
"""
from datetime import datetime
from src.services.database import db


class Vehicle(db.Model):
    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True)

    # 车辆基本信息
    make = db.Column(db.String(50), nullable=False)  # 品牌，如：Toyota
    model = db.Column(db.String(50), nullable=False)  # 型号，如：Camry
    year = db.Column(db.Integer)  # 年份
    color = db.Column(db.String(30))
    license_plate = db.Column(db.String(20), unique=True, nullable=False)

    # 车辆分类
    vehicle_type = db.Column(db.String(30), default='standard')  # standard, premium, luxury, etc.
    capacity = db.Column(db.Integer, default=4)  # 乘客容量

    # 车辆状态
    is_active = db.Column(db.Boolean, default=True)
    last_maintenance = db.Column(db.DateTime)
    next_maintenance = db.Column(db.DateTime)

    # 车辆认证信息
    registration_number = db.Column(db.String(50), unique=True)
    insurance_provider = db.Column(db.String(100))
    insurance_expiry = db.Column(db.DateTime)

    # 车辆位置（如果安装了GPS设备）
    current_lat = db.Column(db.Float)
    current_lng = db.Column(db.Float)
    last_location_update = db.Column(db.DateTime)

    # 统计信息
    total_rides = db.Column(db.Integer, default=0)
    total_distance = db.Column(db.Float, default=0.0)  # 总行驶里程（公里）
    average_rating = db.Column(db.Float, default=5.0)

    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    # 一个车辆只能由一个司机驾驶（一对一关系）

    def to_dict(self):
        """将车辆对象转换为字典格式"""
        return {
            'id': self.id,
            'make': self.make,
            'model': self.model,
            'year': self.year,
            'color': self.color,
            'license_plate': self.license_plate,
            'vehicle_type': self.vehicle_type,
            'capacity': self.capacity,
            'is_active': self.is_active,
            'total_rides': self.total_rides,
            'average_rating': self.average_rating,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def update_location(self, lat, lng):
        """更新车辆位置"""
        self.current_lat = lat
        self.current_lng = lng
        self.last_location_update = datetime.utcnow()
        db.session.commit()

    def increment_rides(self, distance=0):
        """增加行程计数和里程"""
        self.total_rides += 1
        if distance:
            self.total_distance += distance
        db.session.commit()

    def update_rating(self, new_rating):
        """更新车辆平均评分"""
        if self.average_rating == 5.0 and self.total_rides == 0:
            self.average_rating = new_rating
        else:
            # 计算新的平均分
            total_score = self.average_rating * (self.total_rides - 1) + new_rating
            self.average_rating = total_score / self.total_rides
        db.session.commit()

    def __repr__(self):
        return f'<Vehicle {self.make} {self.model} - {self.license_plate}>'