"""
验证器模块 - 数据验证工具
"""
import re


class Validators:
    """验证器类"""

    @staticmethod
    def validate_coordinates(lat: float, lng: float) -> bool:
        """验证坐标是否有效

        Args:
            lat: 纬度
            lng: 经度

        Returns:
            是否有效
        """
        # 纬度范围：-90 到 90
        # 经度范围：-180 到 180
        if not isinstance(lat, (int, float)) or not isinstance(lng, (int, float)):
            return False

        return -90 <= lat <= 90 and -180 <= lng <= 180

    @staticmethod
    def validate_username(username: str) -> tuple[bool, str]:
        """验证用户名

        Args:
            username: 用户名

        Returns:
            (是否有效, 错误信息)
        """
        if not username:
            return False, "用户名不能为空"

        if len(username) < 3:
            return False, "用户名必须至少3个字符"

        if len(username) > 50:
            return False, "用户名不能超过50个字符"

        # 只允许字母、数字、下划线和点
        pattern = r'^[a-zA-Z0-9_.]+$'
        if not re.match(pattern, username):
            return False, "用户名只能包含字母、数字、下划线和点"

        return True, "用户名有效"

    @staticmethod
    def validate_address(address: str) -> tuple[bool, str]:
        """验证地址

        Args:
            address: 地址

        Returns:
            (是否有效, 错误信息)
        """
        if not address:
            return False, "地址不能为空"

        if len(address) < 5:
            return False, "地址必须至少5个字符"

        if len(address) > 200:
            return False, "地址不能超过200个字符"

        return True, "地址有效"

    @staticmethod
    def validate_fare(fare: float) -> tuple[bool, str]:
        """验证费用

        Args:
            fare: 费用

        Returns:
            (是否有效, 错误信息)
        """
        if not isinstance(fare, (int, float)):
            return False, "费用必须是数字"

        if fare < 0:
            return False, "费用不能为负数"

        if fare > 10000:  # 假设最大费用为10000
            return False, "费用不能超过10000"

        return True, "费用有效"

    @staticmethod
    def validate_rating(rating: int) -> tuple[bool, str]:
        """验证评分

        Args:
            rating: 评分（1-5）

        Returns:
            (是否有效, 错误信息)
        """
        if not isinstance(rating, int):
            return False, "评分必须是整数"

        if rating < 1 or rating > 5:
            return False, "评分必须在1到5之间"

        return True, "评分有效"


# 创建验证器实例
validators = Validators()

# 导出函数
validate_coordinates = validators.validate_coordinates
validate_username = validators.validate_username
validate_address = validators.validate_address
validate_fare = validators.validate_fare
validate_rating = validators.validate_rating

# 导出类
__all__ = [
    'Validators',
    'validators',
    'validate_coordinates',
    'validate_username',
    'validate_address',
    'validate_fare',
    'validate_rating'
]