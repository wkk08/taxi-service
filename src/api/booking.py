"""
预订API - 行程管理
"""
from flask import Blueprint, request, jsonify

booking_bp = Blueprint('booking', __name__)


@booking_bp.route('/ride/request', methods=['POST'])
def request_ride():
    """请求行程"""
    try:
        data = request.get_json()

        # 简化逻辑
        return jsonify({
            "success": True,
            "message": "行程请求功能待实现",
            "ride_id": 123,
            "estimated_wait_time": "5-10 minutes"
        }), 201

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"请求行程失败: {str(e)}"
        }), 500


@booking_bp.route('/ride/<int:ride_id>', methods=['GET'])
def get_ride(ride_id):
    """获取行程详情"""
    return jsonify({
        "success": True,
        "ride_id": ride_id,
        "status": "requested",
        "message": "获取行程详情功能待实现"
    })


@booking_bp.route('/ride/<int:ride_id>/cancel', methods=['POST'])
def cancel_ride(ride_id):
    """取消行程"""
    return jsonify({
        "success": True,
        "ride_id": ride_id,
        "message": "行程已取消（模拟）"
    })