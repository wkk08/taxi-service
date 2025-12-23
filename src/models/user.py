from datetime import datetime
from src.services.database import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    phone = db.Column(db.String(20))
    role = db.Column(db.String(20), nullable=False)  # 'passenger' or 'driver'
    
    # 乘客特有字段
    payment_method = db.Column(db.String(50))
    
    # 司机特有字段
    driver_id = db.Column(db.String(50), unique=True)
    license_number = db.Column(db.String(50))
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'))
    current_location = db.Column(db.String(100))
    is_available = db.Column(db.Boolean, default=True)
    rating = db.Column(db.Float, default=5.0)
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    vehicle = db.relationship('Vehicle', backref='driver', uselist=False)
    rides_as_passenger = db.relationship('Ride', foreign_keys='Ride.passenger_id', backref='passenger')
    rides_as_driver = db.relationship('Ride', foreign_keys='Ride.driver_id', backref='driver')
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'phone': self.phone,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Ride:
    pass