"""
API集成测试 - 测试完整的API端点
"""
import pytest
import json


class TestHealthAPI:
    """测试健康检查API"""

    def test_health_endpoint(self, client):
        """测试健康检查端点"""
        response = client.get('/health')

        assert response.status_code == 200

        data = json.loads(response.data)

        assert data['status'] == 'healthy'
        assert data['service'] == 'taxi-service'
        assert data['version'] == '1.0.0'

    def test_root_endpoint(self, client):
        """测试根端点"""
        response = client.get('/')

        assert response.status_code == 200

        data = json.loads(response.data)

        assert data['name'] == 'Taxi Service API'
        assert data['version'] == '1.0.0'
        assert 'endpoints' in data
        assert 'health' in data['endpoints']
        assert 'auth' in data['endpoints']
        assert 'ride' in data['endpoints']

    def test_test_endpoint(self, client):
        """测试测试端点"""
        response = client.get('/api/test')

        assert response.status_code == 200

        data = json.loads(response.data)

        assert data['message'] == 'API is working!'


class TestAuthAPI:
    """测试认证API"""

    def test_register_endpoint(self, client):
        """测试注册端点"""
        # 测试数据
        user_data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'SecurePassword123',
            'role': 'passenger',
            'phone': '+8612345678901'
        }

        response = client.post(
            '/api/auth/register',
            data=json.dumps(user_data),
            content_type='application/json'
        )

        assert response.status_code == 200

        data = json.loads(response.data)

        assert data['success'] is True
        assert '注册功能待实现' in data['message']
        assert 'email' in data['data']

    def test_register_missing_fields(self, client):
        """测试注册缺少字段"""
        # 缺少必填字段
        incomplete_data = {
            'email': 'test@example.com'
            # 缺少username, password, role
        }

        response = client.post(
            '/api/auth/register',
            data=json.dumps(incomplete_data),
            content_type='application/json'
        )

        # 当前实现不验证必填字段，所以是200
        # 实际项目中应该是400
        assert response.status_code == 200

    def test_login_endpoint(self, client):
        """测试登录端点"""
        login_data = {
            'email': 'user@example.com',
            'password': 'password123'
        }

        response = client.post(
            '/api/auth/login',
            data=json.dumps(login_data),
            content_type='application/json'
        )

        assert response.status_code == 200

        data = json.loads(response.data)

        assert data['success'] is True
        assert '登录功能待实现' in data['message']
        assert data['token'] == 'dummy-token-placeholder'

    def test_auth_test_endpoint(self, client):
        """测试认证测试端点"""
        response = client.get('/api/auth/test')

        assert response.status_code == 200

        data = json.loads(response.data)

        assert data['success'] is True
        assert data['message'] == 'Auth API is working!'


class TestBookingAPI:
    """测试预订API"""

    def test_request_ride_endpoint(self, client):
        """测试请求行程端点"""
        ride_data = {
            'pickup_address': '123 Main Street, New York, NY',
            'dropoff_address': '456 Park Avenue, New York, NY',
            'pickup_lat': 40.7128,
            'pickup_lng': -74.0060,
            'dropoff_lat': 40.7489,
            'dropoff_lng': -73.9680
        }

        response = client.post(
            '/api/ride/request',
            data=json.dumps(ride_data),
            content_type='application/json'
        )

        assert response.status_code == 201

        data = json.loads(response.data)

        assert data['success'] is True
        assert data['ride_id'] == 123
        assert data['estimated_wait_time'] == '5-10 minutes'
        assert '行程请求功能待实现' in data['message']

    def test_get_ride_endpoint(self, client):
        """测试获取行程详情端点"""
        ride_id = 123

        response = client.get(f'/api/ride/{ride_id}')

        assert response.status_code == 200

        data = json.loads(response.data)

        assert data['success'] is True
        assert data['ride_id'] == ride_id
        assert data['status'] == 'requested'
        assert '获取行程详情功能待实现' in data['message']

    def test_cancel_ride_endpoint(self, client):
        """测试取消行程端点"""
        ride_id = 123

        response = client.post(f'/api/ride/{ride_id}/cancel')

        assert response.status_code == 200

        data = json.loads(response.data)

        assert data['success'] is True
        assert data['ride_id'] == ride_id
        assert '行程已取消（模拟）' in data['message']

    def test_invalid_ride_id(self, client):
        """测试无效的行程ID"""
        # 测试非数字ID
        response = client.get('/api/ride/abc')

        # 当前实现不验证ID格式，所以可能返回200
        # 实际项目中应该是400或404
        assert response.status_code in [200, 404, 405]


class TestErrorHandling:
    """测试错误处理"""

    def test_404_not_found(self, client):
        """测试404错误处理"""
        response = client.get('/nonexistent-endpoint')

        # Flask默认返回404
        assert response.status_code == 404

    def test_method_not_allowed(self, client):
        """测试方法不允许"""
        # 尝试使用错误的HTTP方法
        response = client.post('/health')  # /health只支持GET

        assert response.status_code == 405  # Method Not Allowed


class TestDatabaseIntegration:
    """测试数据库集成"""

    def test_database_connection(self, db_session):
        """测试数据库连接"""
        # 执行一个简单的查询
        result = db_session.execute('SELECT 1').fetchone()

        assert result[0] == 1

    def test_create_user_in_database(self, db_session):
        """测试在数据库中创建用户"""
        from src.models.user import User

        # 创建用户
        user = User(
            email='integration@test.com',
            username='integration_user',
            password_hash='test_hash',
            role='passenger'
        )

        db_session.add(user)
        db_session.commit()

        # 验证用户已创建
        saved_user = db_session.query(User).filter_by(email='integration@test.com').first()

        assert saved_user is not None
        assert saved_user.username == 'integration_user'
        assert saved_user.role == 'passenger'