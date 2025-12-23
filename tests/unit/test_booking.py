"""
预订单元测试 - 测试预订相关功能
"""
import pytest
from src.services.location import LocationService
from src.services.payment import PaymentService
from src.services.notification import NotificationService


class TestLocationService:
    """测试位置服务"""

    def test_calculate_distance(self):
        """测试距离计算"""
        # 纽约坐标
        ny_lat, ny_lng = 40.7128, -74.0060

        # 洛杉矶坐标
        la_lat, la_lng = 34.0522, -118.2437

        # 计算距离
        distance = LocationService.calculate_distance(ny_lat, ny_lng, la_lat, la_lng)

        # 纽约到洛杉矶大约3935公里
        assert isinstance(distance, float)
        assert distance > 3900 and distance < 4000

        # 测试相同点
        same_distance = LocationService.calculate_distance(ny_lat, ny_lng, ny_lat, ny_lng)
        assert same_distance == 0.0

    def test_estimate_travel_time(self):
        """测试行驶时间估算"""
        distance_km = 100

        # 正常交通
        time_normal = LocationService.estimate_travel_time(distance_km, traffic_factor=1.0)
        assert time_normal == 120.0  # 100km / 50km/h = 2小时 = 120分钟

        # 交通拥堵
        time_traffic = LocationService.estimate_travel_time(distance_km, traffic_factor=1.5)
        assert time_traffic == 180.0  # 增加50%

        # 交通顺畅
        time_smooth = LocationService.estimate_travel_time(distance_km, traffic_factor=0.8)
        assert time_smooth == 96.0  # 减少20%

    def test_find_nearby_drivers(self):
        """测试查找附近司机"""
        # 纽约坐标
        ny_lat, ny_lng = 40.7128, -74.0060

        drivers = LocationService.find_nearby_drivers(ny_lat, ny_lng)

        assert isinstance(drivers, list)

        if drivers:  # 如果有模拟数据
            driver = drivers[0]
            assert 'driver_id' in driver
            assert 'name' in driver
            assert 'distance_km' in driver
            assert 'eta_minutes' in driver
            assert 'rating' in driver

    def test_validate_coordinates(self):
        """测试坐标验证"""
        # 有效坐标
        assert LocationService.validate_coordinates(40.7128, -74.0060) is True
        assert LocationService.validate_coordinates(0, 0) is True
        assert LocationService.validate_coordinates(-90, -180) is True
        assert LocationService.validate_coordinates(90, 180) is True

        # 无效坐标
        assert LocationService.validate_coordinates(100, 50) is False  # 纬度超过90
        assert LocationService.validate_coordinates(50, 200) is False  # 经度超过180
        assert LocationService.validate_coordinates(-100, 50) is False  # 纬度小于-90
        assert LocationService.validate_coordinates(50, -200) is False  # 经度小于-180
        assert LocationService.validate_coordinates('invalid', 50) is False  # 非数字


class TestPaymentService:
    """测试支付服务"""

    def test_calculate_fare(self):
        """测试车费计算"""
        # 基础测试
        fare = PaymentService.calculate_fare(10.0)
        assert fare == 17.5  # 2.5 + (10 * 1.5)

        # 自定义费率
        fare_custom = PaymentService.calculate_fare(20.0, base_rate=5.0, per_km_rate=2.0)
        assert fare_custom == 45.0  # 5 + (20 * 2)

        # 零距离
        fare_zero = PaymentService.calculate_fare(0)
        assert fare_zero == 2.5  # 只有基础费用

    def test_estimate_fare(self):
        """测试预估车费"""
        # 纽约坐标
        ny_lat, ny_lng = 40.7128, -74.0060

        # 新泽西坐标
        nj_lat, nj_lng = 40.7589, -74.0567

        estimate = PaymentService.estimate_fare(ny_lat, ny_lng, nj_lat, nj_lng)

        assert isinstance(estimate, dict)
        assert 'estimated_fare' in estimate
        assert 'currency' in estimate
        assert 'distance_km' in estimate
        assert 'base_fare' in estimate
        assert 'distance_fare' in estimate
        assert 'message' in estimate

        assert estimate['currency'] == 'CNY'
        assert estimate['estimated_fare'] == 25.0  # 根据我们的模拟数据

    def test_process_payment(self):
        """测试支付处理"""
        amount = 100.0

        result = PaymentService.process_payment(amount)

        assert isinstance(result, dict)
        assert result['success'] is True
        assert 'transaction_id' in result
        assert result['amount'] == amount
        assert result['currency'] == 'CNY'
        assert result['payment_method'] == 'credit_card'
        assert result['status'] == 'completed'
        assert 'timestamp' in result

        # 测试其他支付方式
        result_cash = PaymentService.process_payment(50.0, 'cash')
        assert result_cash['payment_method'] == 'cash'

    def test_refund_payment(self):
        """测试退款处理"""
        transaction_id = 'txn_123456'

        result = PaymentService.refund_payment(transaction_id)

        assert isinstance(result, dict)
        assert result['success'] is True
        assert 'refund_id' in result
        assert result['original_transaction_id'] == transaction_id
        assert 'refund_amount' in result
        assert result['status'] == 'refunded'
        assert 'message' in result

        # 测试部分退款
        result_partial = PaymentService.refund_payment(transaction_id, amount=50.0)
        assert result_partial['refund_amount'] == 50.0


class TestNotificationService:
    """测试通知服务"""

    def test_send_ride_request_notification(self):
        """测试发送行程请求通知"""
        # 这个测试主要是确保函数能够正常执行
        result = NotificationService.send_ride_request_notification(
            driver_id=1,
            passenger_name='张三',
            pickup_location='123 Main St'
        )

        assert result is True

    def test_send_ride_accepted_notification(self):
        """测试发送行程接受通知"""
        result = NotificationService.send_ride_accepted_notification(
            passenger_id=2,
            driver_name='李师傅',
            eta_minutes=5
        )

        assert result is True

    def test_send_ride_completed_notification(self):
        """测试发送行程完成通知"""
        result = NotificationService.send_ride_completed_notification(
            passenger_id=3,
            driver_id=4,
            fare=35.5
        )

        assert result is True

    def test_send_payment_notification(self):
        """测试发送支付通知"""
        # 支付通知
        result_payment = NotificationService.send_payment_notification(
            user_id=5,
            amount=100.0,
            transaction_type='payment'
        )

        assert result_payment is True

        # 退款通知
        result_refund = NotificationService.send_payment_notification(
            user_id=6,
            amount=50.0,
            transaction_type='refund'
        )

        assert result_refund is True