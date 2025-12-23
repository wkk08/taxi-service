from flask import Blueprint, request, jsonify
import datetime
from src.utils.security import token_required, role_required
from src.models.user import User
from src.models.ride import Ride
from src.services.database import db
from src.services.location import LocationService

driver_bp = Blueprint('driver', __name__)

# 创建一个简化的通知服务
class SimpleNotificationService:
    @staticmethod
    def send_ride_status_notification(user_id, ride_id, status, message=""):
        print(f"通知: 用户 {user_id} 的行程 {ride_id} 状态更新为 {status}: {message}")
        return True

notification_service = SimpleNotificationService()




@driver_bp.route('/location/update', methods=['POST'])
@token_required
@role_required('driver')
def update_location():
    """司机更新位置"""
    try:
        data = request.get_json()

        # 验证必填字段
        if 'latitude' not in data or 'longitude' not in data:
            return jsonify({'error': 'Latitude and longitude are required'}), 400

        # 获取司机信息
        driver = User.query.get(request.user_id)
        if not driver:
            return jsonify({'error': 'Driver not found'}), 404

        # 更新位置
        driver.current_location = f"{data['latitude']},{data['longitude']}"

        # 如果有地址信息，也更新
        if 'address' in data:
            # 这里可以存储地址，但我们的模型只存储坐标字符串
            pass

        db.session.commit()

        return jsonify({
            'message': 'Location updated successfully',
            'location': driver.current_location
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@driver_bp.route('/available', methods=['POST'])
@token_required
@role_required('driver')
def set_availability():
    """设置司机可用状态"""
    try:
        data = request.get_json()

        # 验证必填字段
        if 'is_available' not in data:
            return jsonify({'error': 'is_available field is required'}), 400

        # 获取司机信息
        driver = User.query.get(request.user_id)
        if not driver:
            return jsonify({'error': 'Driver not found'}), 404

        # 更新可用状态
        driver.is_available = bool(data['is_available'])

        db.session.commit()

        return jsonify({
            'message': 'Availability updated successfully',
            'is_available': driver.is_available
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@driver_bp.route('/ride/<int:ride_id>/accept', methods=['POST'])
@token_required
@role_required('driver')
def accept_ride(ride_id):
    """司机接受行程"""
    try:
        # 获取行程信息
        ride = Ride.query.get(ride_id)
        if not ride:
            return jsonify({'error': 'Ride not found'}), 404

        # 检查行程状态
        if ride.status != 'requested':
            return jsonify({'error': f'Cannot accept a ride with status: {ride.status}'}), 400

        # 获取司机信息
        driver = User.query.get(request.user_id)
        if not driver:
            return jsonify({'error': 'Driver not found'}), 404

        # 检查司机是否可用
        if not driver.is_available:
            return jsonify({'error': 'Driver is not available'}), 400

        # 更新行程信息
        ride.driver_id = driver.id
        ride.status = 'accepted'
        ride.accepted_at = datetime.datetime.utcnow()

        # 更新司机状态为不可用
        driver.is_available = False

        # 发送通知给乘客
        notification_service.send_ride_status_notification(
            ride.passenger_id,
            ride.id,
            'accepted',
            f'Driver {driver.username} has accepted your ride'
        )

        db.session.commit()

        return jsonify({
            'message': 'Ride accepted successfully',
            'ride': ride.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@driver_bp.route('/ride/<int:ride_id>/start', methods=['POST'])
@token_required
@role_required('driver')
def start_ride(ride_id):
    """司机开始行程"""
    try:
        # 获取行程信息
        ride = Ride.query.get(ride_id)
        if not ride:
            return jsonify({'error': 'Ride not found'}), 404

        # 检查行程状态
        if ride.status != 'accepted':
            return jsonify({'error': f'Cannot start a ride with status: {ride.status}'}), 400

        # 检查司机是否有权开始此行程
        if ride.driver_id != request.user_id:
            return jsonify({'error': 'Unauthorized to start this ride'}), 403

        # 更新行程状态
        ride.status = 'in_progress'
        ride.started_at = datetime.datetime.utcnow()

        # 发送通知给乘客
        notification_service.send_ride_status_notification(
            ride.passenger_id,
            ride.id,
            'in_progress',
            'Your ride has started'
        )

        db.session.commit()

        return jsonify({
            'message': 'Ride started successfully',
            'ride': ride.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@driver_bp.route('/ride/<int:ride_id>/complete', methods=['POST'])
@token_required
@role_required('driver')
def complete_ride(ride_id):
    """司机完成行程"""
    try:
        data = request.get_json()

        # 获取行程信息
        ride = Ride.query.get(ride_id)
        if not ride:
            return jsonify({'error': 'Ride not found'}), 404

        # 检查行程状态
        if ride.status != 'in_progress':
            return jsonify({'error': f'Cannot complete a ride with status: {ride.status}'}), 400

        # 检查司机是否有权完成此行程
        if ride.driver_id != request.user_id:
            return jsonify({'error': 'Unauthorized to complete this ride'}), 403

        # 验证必填字段
        if 'actual_fare' not in data:
            return jsonify({'error': 'actual_fare field is required'}), 400

        # 更新行程信息
        ride.status = 'completed'
        ride.actual_fare = float(data['actual_fare'])
        ride.completed_at = datetime.datetime.utcnow()

        # 更新司机状态为可用
        driver = User.query.get(request.user_id)
        if driver:
            driver.is_available = True

        # 发送通知给乘客
        notification_service.send_ride_status_notification(
            ride.passenger_id,
            ride.id,
            'completed',
            f'Your ride has been completed. Fare: ${ride.actual_fare:.2f}'
        )

        db.session.commit()

        return jsonify({
            'message': 'Ride completed successfully',
            'ride': ride.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@driver_bp.route('/rides/active', methods=['GET'])
@token_required
@role_required('driver')
def get_active_rides():
    """获取司机的活跃行程"""
    try:
        # 获取司机的活跃行程
        active_rides = Ride.query.filter(
            Ride.driver_id == request.user_id,
            Ride.status.in_(['accepted', 'in_progress'])
        ).order_by(Ride.requested_at.desc()).all()

        return jsonify({
            'rides': [ride.to_dict() for ride in active_rides]
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@driver_bp.route('/rides/history', methods=['GET'])
@token_required
@role_required('driver')
def get_ride_history():
    """获取司机的行程历史"""
    try:
        # 获取查询参数
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        # 获取司机的历史行程
        query = Ride.query.filter(
            Ride.driver_id == request.user_id,
            Ride.status.in_(['completed', 'cancelled'])
        ).order_by(Ride.completed_at.desc())

        # 分页
        paginated_rides = query.paginate(page=page, per_page=per_page, error_out=False)

        return jsonify({
            'rides': [ride.to_dict() for ride in paginated_rides.items],
            'total': paginated_rides.total,
            'pages': paginated_rides.pages,
            'current_page': paginated_rides.page
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@driver_bp.route('/nearby-requests', methods=['GET'])
@token_required
@role_required('driver')
def get_nearby_ride_requests():
    """获取附近的行程请求"""
    try:
        # 获取司机当前位置
        driver = User.query.get(request.user_id)
        if not driver or not driver.current_location:
            return jsonify({'error': 'Driver location not set'}), 400

        # 解析司机位置
        try:
            lat_str, lon_str = driver.current_location.split(',')
            driver_lat = float(lat_str)
            driver_lon = float(lon_str)
        except (ValueError, AttributeError):
            return jsonify({'error': 'Invalid driver location format'}), 400

        # 获取半径参数
        radius_km = float(request.args.get('radius', 5.0))

        # 获取所有未分配的行程请求
        ride_requests = Ride.query.filter(
            Ride.status == 'requested',
            Ride.driver_id.is_(None)
        ).all()

        # 过滤附近的请求
        nearby_requests = []
        for ride in ride_requests:
            if ride.pickup_lat and ride.pickup_lng:
                distance = LocationService.calculate_distance(
                    driver_lat, driver_lon,
                    ride.pickup_lat, ride.pickup_lng
                )

                if distance <= radius_km:
                    ride_data = ride.to_dict()
                    ride_data['distance_km'] = round(distance, 2)

                    # 估算费用和时间
                    if ride.estimated_fare is None:
                        estimated_time = LocationService.estimate_ride_time(distance)
                        ride_data['estimated_fare'] = LocationService.estimate_ride_fare(distance, estimated_time)
                        ride_data['estimated_time_minutes'] = round(estimated_time, 1)

                    nearby_requests.append(ride_data)

        return jsonify({
            'driver_location': driver.current_location,
            'radius_km': radius_km,
            'nearby_requests': nearby_requests,
            'count': len(nearby_requests)
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500