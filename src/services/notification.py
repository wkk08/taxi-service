"""
通知服务 - 处理用户通知（简化版）
"""


class NotificationService:
    """通知服务类"""

    @staticmethod
    def send_ride_request_notification(driver_id: int, passenger_name: str, pickup_location: str) -> bool:
        """发送行程请求通知给司机

        Args:
            driver_id: 司机ID
            passenger_name: 乘客姓名
            pickup_location: 上车地点

        Returns:
            是否成功
        """
        # 简化版本：打印通知
        # 实际项目中应该使用推送通知、短信或邮件

        print(f"📱 通知司机 {driver_id}: 乘客 {passenger_name} 请求从 {pickup_location} 上车")
        return True

    @staticmethod
    def send_ride_accepted_notification(passenger_id: int, driver_name: str, eta_minutes: int) -> bool:
        """发送行程接受通知给乘客

        Args:
            passenger_id: 乘客ID
            driver_name: 司机姓名
            eta_minutes: 预计到达时间（分钟）

        Returns:
            是否成功
        """
        print(f"📱 通知乘客 {passenger_id}: 司机 {driver_name} 已接受行程，预计 {eta_minutes} 分钟到达")
        return True

    @staticmethod
    def send_ride_completed_notification(passenger_id: int, driver_id: int, fare: float) -> bool:
        """发送行程完成通知

        Args:
            passenger_id: 乘客ID
            driver_id: 司机ID
            fare: 车费

        Returns:
            是否成功
        """
        print(f"📱 通知乘客 {passenger_id} 和司机 {driver_id}: 行程已完成，车费 {fare} 元")
        return True

    @staticmethod
    def send_payment_notification(user_id: int, amount: float, transaction_type: str) -> bool:
        """发送支付通知

        Args:
            user_id: 用户ID
            amount: 金额
            transaction_type: 交易类型（payment/refund）

        Returns:
            是否成功
        """
        if transaction_type == 'payment':
            print(f"💰 通知用户 {user_id}: 支付成功 {amount} 元")
        else:
            print(f"💰 通知用户 {user_id}: 退款成功 {amount} 元")

        return True


# 创建通知服务实例
notification_service = NotificationService()

# 导出
__all__ = [
    'NotificationService',
    'notification_service'
]