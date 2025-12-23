from datetime import datetime
from src.services.database import db

class Ride(db.Model):
    __tablename__ = 'rides'
    
    id = db.Column(db.Integer, primary_key=True)
    passenger_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # 位置信息
    pickup_address = db.Column(db.String(200), nullable=False)
    dropoff_address = db.Column(db.String(200), nullable=False)
    pickup_lat = db.Column(db.Float)
    pickup_lng = db.Column(db.Float)
    dropoff_lat = db.Column(db.Float)
    dropoff_lng = db.Column(db.Float)
    
    # 状态和计时
    status = db.Column(db.String(20), default='requested')  # requested, accepted, in_progress, completed, cancelled
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)
    accepted_at = db.Column(db.DateTime)
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    cancelled_at = db.Column(db.DateTime)
    
    # 费用信息
    estimated_fare = db.Column(db.Float)
    actual_fare = db.Column(db.Float)
    payment_status = db.Column(db.String(20), default='pending')  # pending, paid, refunded
    
    # 评价
    passenger_rating = db.Column(db.Integer)
    driver_rating = db.Column(db.Integer)
    passenger_comment = db.Column(db.Text)
    driver_comment = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'passenger_id': self.passenger_id,
            'driver_id': self.driver_id,
            'pickup_address': self.pickup_address,
            'dropoff_address': self.dropoff_address,
            'status': self.status,
            'estimated_fare': self.estimated_fare,
            'actual_fare': self.actual_fare,
            'requested_at': self.requested_at.isoformat() if self.requested_at else None,
            'accepted_at': self.accepted_at.isoformat() if self.accepted_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }