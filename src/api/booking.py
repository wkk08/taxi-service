from flask import Blueprint, request, jsonify
import jwt
from src.models.user import User
from src.models.ride import Ride
from src.services.database import db

booking_bp = Blueprint('booking', __name__)
SECRET_KEY = 'your-secret-key-here'

def verify_token(token):
    """验证JWT令牌"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@booking_bp.route('/ride/request', methods=['POST'])
def request_ride():
    # 验证身份
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'Authorization token required'}), 401
    
    payload = verify_token(token.replace('Bearer ', ''))
    if not payload or payload['role'] != 'passenger':
        return jsonify({'error': 'Invalid or expired token'}), 401
    
    try:
        data = request.get_json()
        
        # 验证必填字段
        required_fields = ['pickup_address', 'dropoff_address']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # 创建行程
        new_ride = Ride(
            passenger_id=payload['user_id'],
            pickup_address=data['pickup_address'],
            dropoff_address=data['dropoff_address'],
            pickup_lat=data.get('pickup_lat'),
            pickup_lng=data.get('pickup_lng'),
            dropoff_lat=data.get('dropoff_lat'),
            dropoff_lng=data.get('dropoff_lng'),
            estimated_fare=data.get('estimated_fare'),
            status='requested'
        )
        
        db.session.add(new_ride)
        db.session.commit()
        
        # TODO: 这里应该添加司机匹配逻辑
        
        return jsonify({
            'message': 'Ride requested successfully',
            'ride_id': new_ride.id,
            'estimated_wait_time': '5-10 minutes'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@booking_bp.route('/ride/<int:ride_id>', methods=['GET'])
def get_ride(ride_id):
    # 验证身份
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'Authorization token required'}), 401
    
    payload = verify_token(token.replace('Bearer ', ''))
    if not payload:
        return jsonify({'error': 'Invalid or expired token'}), 401
    
    try:
        ride = Ride.query.get(ride_id)
        if not ride:
            return jsonify({'error': 'Ride not found'}), 404
        
        # 检查用户是否有权查看此行程
        if ride.passenger_id != payload['user_id'] and ride.driver_id != payload['user_id']:
            return jsonify({'error': 'Unauthorized to view this ride'}), 403
        
        return jsonify({
            'ride': ride.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@booking_bp.route('/ride/<int:ride_id>/cancel', methods=['POST'])
def cancel_ride(ride_id):
    # 验证身份
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'Authorization token required'}), 401
    
    payload = verify_token(token.replace('Bearer ', ''))
    if not payload:
        return jsonify({'error': 'Invalid or expired token'}), 401
    
    try:
        ride = Ride.query.get(ride_id)
        if not ride:
            return jsonify({'error': 'Ride not found'}), 404
        
        # 检查用户是否有权取消此行程
        if ride.passenger_id != payload['user_id']:
            return jsonify({'error': 'Only the passenger can cancel this ride'}), 403
        
        # 检查状态
        if ride.status in ['completed', 'cancelled']:
            return jsonify({'error': f'Cannot cancel a {ride.status} ride'}), 400
        
        # 更新行程状态
        ride.status = 'cancelled'
        ride.cancelled_at = datetime.datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Ride cancelled successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500