"""
模型单元测试 - 测试数据模型
"""
import pytest
from datetime import datetime
from src.models.user import User
from src.models.ride import Ride
from src.models.vehicle import Vehicle


class TestUserModel:
    """测试用户模型"""

    def test_create_user(self, db_session):
        """测试创建用户"""
        user = User(
            email='test@example.com',
            username='testuser',
            password_hash='hashed_password',
            role='passenger',
            phone='+1234567890'
        )

        db_session.add(user)
        db_session.commit()

        assert user.id is not None
        assert user.email == 'test@example.com'
        assert user.role == 'passenger'
        assert user.created_at is not None

    def test_user_to_dict(self, db_session):
        """测试用户转字典方法"""
        user = User(
            email='test2@example.com',
            username='testuser2',
            password_hash='hashed_password2',
            role='driver'
        )

        db_session.add(user)
        db_session.commit()

        user_dict = user.to_dict()

        assert isinstance(user_dict, dict)
        assert 'id' in user_dict
        assert user_dict['email'] == 'test2@example.com'
        assert user_dict['role'] == 'driver'

    def test_create_driver_user(self, db_session):
        """测试创建司机用户"""
        # 先创建车辆
        vehicle = Vehicle(
            make='Toyota',
            model='Camry',
            year=2020,
            color='White',
            license_plate='ABC123',
            vehicle_type='standard'
        )
        db_session.add(vehicle)
        db_session.flush()  # 获取车辆ID但不提交

        # 创建司机
        driver = User(
            email='driver@example.com',
            username='driver1',
            password_hash='hashed_password',
            role='driver',
            driver_id='DRV001',
            license_number='LN123456',
            vehicle_id=vehicle.id,
            current_location='40.7128,-74.0060',
            is_available=True,
            rating=4.8
        )

        db_session.add(driver)
        db_session.commit()

        assert driver.role == 'driver'
        assert driver.is_available is True
        assert driver.vehicle_id == vehicle.id
        assert driver.current_location is not None


class TestRideModel:
    """测试行程模型"""

    def test_create_ride(self, db_session):
        """测试创建行程"""
        # 创建乘客
        passenger = User(
            email='passenger@example.com',
            username='passenger1',
            password_hash='hashed_password',
            role='passenger'
        )
        db_session.add(passenger)
        db_session.flush()

        # 创建司机
        driver = User(
            email='driver2@example.com',
            username='driver2',
            password_hash='hashed_password',
            role='driver'
        )
        db_session.add(driver)
        db_session.flush()

        # 创建行程
        ride = Ride(
            passenger_id=passenger.id,
            driver_id=driver.id,
            pickup_address='123 Main St, New York, NY',
            dropoff_address='456 Park Ave, New York, NY',
            pickup_lat=40.7128,
            pickup_lng=-74.0060,
            dropoff_lat=40.7489,
            dropoff_lng=-73.9680,
            status='requested',
            estimated_fare=25.0
        )

        db_session.add(ride)
        db_session.commit()

        assert ride.id is not None
        assert ride.status == 'requested'
        assert ride.estimated_fare == 25.0
        assert ride.pickup_address is not None
        assert ride.dropoff_address is not None

    def test_ride_status_transitions(self, db_session):
        """测试行程状态转换"""
        # 创建测试数据
        passenger = User(
            email='p2@example.com',
            username='p2',
            password_hash='hash',
            role='passenger'
        )
        driver = User(
            email='d2@example.com',
            username='d2',
            password_hash='hash',
            role='driver'
        )
        db_session.add_all([passenger, driver])
        db_session.flush()

        ride = Ride(
            passenger_id=passenger.id,
            pickup_address='Test Pickup',
            dropoff_address='Test Dropoff',
            status='requested'
        )
        db_session.add(ride)
        db_session.commit()

        # 测试状态转换
        assert ride.status == 'requested'

        # 司机接单
        ride.driver_id = driver.id
        ride.status = 'accepted'
        ride.accepted_at = datetime.utcnow()
        db_session.commit()

        assert ride.status == 'accepted'
        assert ride.accepted_at is not None

        # 行程开始
        ride.status = 'in_progress'
        ride.started_at = datetime.utcnow()
        db_session.commit()

        assert ride.status == 'in_progress'
        assert ride.started_at is not None

        # 行程完成
        ride.status = 'completed'
        ride.completed_at = datetime.utcnow()
        ride.actual_fare = 30.0
        ride.payment_status = 'paid'
        db_session.commit()

        assert ride.status == 'completed'
        assert ride.actual_fare == 30.0
        assert ride.payment_status == 'paid'

    def test_ride_to_dict(self, db_session):
        """测试行程转字典方法"""
        passenger = User(
            email='p3@example.com',
            username='p3',
            password_hash='hash',
            role='passenger'
        )
        db_session.add(passenger)
        db_session.flush()

        ride = Ride(
            passenger_id=passenger.id,
            pickup_address='Pickup St',
            dropoff_address='Dropoff Ave',
            status='requested'
        )
        db_session.add(ride)
        db_session.commit()

        ride_dict = ride.to_dict()

        assert isinstance(ride_dict, dict)
        assert 'id' in ride_dict
        assert ride_dict['status'] == 'requested'
        assert ride_dict['pickup_address'] == 'Pickup St'
        assert 'requested_at' in ride_dict


class TestVehicleModel:
    """测试车辆模型"""

    def test_create_vehicle(self, db_session):
        """测试创建车辆"""
        vehicle = Vehicle(
            make='Honda',
            model='Accord',
            year=2021,
            color='Black',
            license_plate='XYZ789',
            vehicle_type='premium',
            capacity=4,
            is_active=True
        )

        db_session.add(vehicle)
        db_session.commit()

        assert vehicle.id is not None
        assert vehicle.make == 'Honda'
        assert vehicle.model == 'Accord'
        assert vehicle.license_plate == 'XYZ789'
        assert vehicle.is_active is True

    def test_vehicle_to_dict(self, db_session):
        """测试车辆转字典方法"""
        vehicle = Vehicle(
            make='BMW',
            model='X5',
            year=2022,
            color='Blue',
            license_plate='BMW001',
            vehicle_type='luxury'
        )

        db_session.add(vehicle)
        db_session.commit()

        vehicle_dict = vehicle.to_dict()

        assert isinstance(vehicle_dict, dict)
        assert 'id' in vehicle_dict
        assert vehicle_dict['make'] == 'BMW'
        assert vehicle_dict['model'] == 'X5'
        assert vehicle_dict['vehicle_type'] == 'luxury'

    def test_vehicle_update_location(self, db_session):
        """测试更新车辆位置"""
        vehicle = Vehicle(
            make='Tesla',
            model='Model 3',
            license_plate='TES001'
        )
        db_session.add(vehicle)
        db_session.commit()

        # 初始位置应该为空
        assert vehicle.current_lat is None
        assert vehicle.current_lng is None

        # 更新位置
        vehicle.update_location(40.7580, -73.9855)

        assert vehicle.current_lat == 40.7580
        assert vehicle.current_lng == -73.9855
        assert vehicle.last_location_update is not None

    def test_vehicle_increment_rides(self, db_session):
        """测试增加行程计数"""
        vehicle = Vehicle(
            make='Ford',
            model='Focus',
            license_plate='FORD001'
        )
        db_session.add(vehicle)
        db_session.commit()

        # 初始值
        assert vehicle.total_rides == 0
        assert vehicle.total_distance == 0.0

        # 增加行程
        vehicle.increment_rides(distance=15.5)

        assert vehicle.total_rides == 1
        assert vehicle.total_distance == 15.5

        # 再次增加
        vehicle.increment_rides(distance=10.2)

        assert vehicle.total_rides == 2
        assert vehicle.total_distance == 25.7

    def test_vehicle_update_rating(self, db_session):
        """测试更新车辆评分"""
        vehicle = Vehicle(
            make='Audi',
            model='A4',
            license_plate='AUDI001'
        )
        db_session.add(vehicle)
        db_session.commit()

        # 初始评分
        assert vehicle.average_rating == 5.0
        assert vehicle.total_rides == 0

        # 增加行程并更新评分
        vehicle.increment_rides(distance=0)
        vehicle.update_rating(4.5)

        assert vehicle.total_rides == 1
        assert vehicle.average_rating == 4.5

        # 第二次评分
        vehicle.increment_rides(distance=0)
        vehicle.update_rating(5.0)

        # 平均分应该是 (4.5 + 5.0) / 2 = 4.75
        assert vehicle.total_rides == 2
        assert vehicle.average_rating == 4.75