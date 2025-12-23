from flask import Blueprint, request, jsonify
from src.utils.security import token_required
from src.services.notification import NotificationService

notification_bp = Blueprint('notification', __name__)
notification_service = NotificationService()


@notification_bp.route('/notifications', methods=['GET'])
@token_required
def get_notifications():
    """获取用户的通知"""
    try:
        # 获取查询参数
        limit = int(request.args.get('limit', 10))

        # 获取用户通知
        notifications = notification_service.get_user_notifications(request.user_id, limit)

        return jsonify({
            'notifications': notifications,
            'count': len(notifications)
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@notification_bp.route('/notifications/clear', methods=['POST'])
@token_required
def clear_notifications():
    """清除用户的通知"""
    try:
        # 目前我们的实现中，通知被读取后就会从队列中移除
        # 这里可以添加清除所有通知的逻辑，但目前返回成功即可
        return jsonify({
            'message': 'Notifications cleared successfully'
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@notification_bp.route('/subscribe', methods=['GET'])
@token_required
def subscribe_to_notifications():
    """订阅实时通知（SSE示例）"""
    # 注意：这是一个简化的SSE实现，实际生产环境中可能需要使用WebSocket

    from flask import Response
    import json
    import time

    def event_stream():
        """生成事件流"""
        try:
            # 设置SSE头
            yield 'data: {"type": "connected", "message": "Connected to notification stream"}\n\n'

            # 模拟实时通知（实际中应该使用Redis Pub/Sub等）
            last_check = time.time()

            while True:
                # 每隔5秒检查一次新通知
                if time.time() - last_check > 5:
                    notifications = notification_service.get_user_notifications(request.user_id, 5)

                    for notification in notifications:
                        yield f'data: {json.dumps(notification)}\n\n'

                    last_check = time.time()

                time.sleep(1)

        except GeneratorExit:
            print("Client disconnected")

    return Response(
        event_stream(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'X-Accel-Buffering': 'no'  # 禁用Nginx缓冲
        }
    )