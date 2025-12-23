"""
位置服务 - 处理地理位置相关逻辑（简化版）
"""
import math

class LocationService:
    """位置服务类"""

    @staticmethod
    def calculate_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """计算两个坐标点之间的距离（使用Haversine公式）

        Args:
            lat1: 纬度1
            lng1: 经度1
            lat2: 纬度2
            lng2: 经度2

        Returns:
            距离（公里）
        """
        # 将角度转换为弧度
        lat1_rad = math.radians(lat1)
        lng1_rad = math.radians(lng1)
        lat2_rad = math.radians(lat2)
        lng2_rad = math.radians(lng2)

        # Haversine公式
        dlat = lat2_rad - lat1_rad
        dlng = lng2_rad - lng1_rad
        a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng/2)**2
        c = 2 * math.asin(math.sqrt(a))

        # 地球半径（公里）
        r = 6371

        return c * r

    @staticmethod
    def find_nearby_drivers(lat: float, lng: float, radius_km: float = 5, limit: int = 10) -> list:
        """查找附近的司机（简化版）

        Args:
            lat: 纬度
            lng: 经度
            radius_km: 搜索半径（公里）
            limit: 返回数量限制

        Returns:
            司机列表
        """
        # 简化版本：返回空列表或模拟数据
        # 实际项目中应该使用空间数据库查询

        return [
            {
                'driver_id': 1,
                'name': '司机张三',
                'distance_km': 1.5,
                'eta_minutes': 5,
                'rating': 4.8
            },
            {
                'driver_id': 2,
                'name': '司机李四',
                'distance_km': 2.3,
                'eta_minutes': 8,
                'rating': 4.9
            }
        ]

    @staticmethod
    def estimate_travel_time(distance_km: float, traffic_factor: float = 1.0) -> float:
        """估计行驶时间

        Args:
            distance_km: 距离（公里）
            traffic_factor: 交通系数（1.0表示正常交通）

        Returns:
            行驶时间（分钟）
        """
        # 假设平均速度50km/h
        average_speed = 50  # km/h
        base_time_hours = distance_km / average_speed
        adjusted_time_hours = base_time_hours * traffic_factor

        # 转换为分钟
        return adjusted_time_hours * 60

    @staticmethod
    def validate_coordinates(lat: float, lng: float) -> bool:
        """验证坐标是否有效

        Args:
            lat: 纬度
            lng: 经度

        Returns:
            是否有效
        """
        if not isinstance(lat, (int, float)) or not isinstance(lng, (int, float)):
            return False

        return -90 <= lat <= 90 and -180 <= lng <= 180

# 创建位置服务实例
location_service = LocationService()

# 导出
__all__ = [
    'LocationService',
    'location_service'
]