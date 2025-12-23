from flask import Flask, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from src.utils.config import Config

# 加载环境变量
load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # 配置应用
    app.config.from_object(Config)
    
    # 注册蓝图
    from src.api.auth import auth_bp
    from src.api.booking import booking_bp
    from src.api.driver import driver_bp
    from src.api.notification import notification_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(booking_bp, url_prefix='/api')
    app.register_blueprint(driver_bp, url_prefix='/api/driver')
    app.register_blueprint(notification_bp, url_prefix='/api')
    
    # 健康检查端点
    @app.route('/health')
    def health():
        return jsonify({
            "status": "healthy",
            "service": "taxi-service",
            "version": os.getenv("APP_VERSION", "1.0.0")
        })
    
    # 根路径
    @app.route('/')
    def index():
        return jsonify({
            "name": "Taxi Service API",
            "version": "1.0.0",
            "endpoints": [
                "/api/auth/register",
                "/api/auth/login",
                "/api/ride/request",
                "/api/ride/<id>",
                "/api/driver/location",
                "/api/driver/available",
                "/health"
            ]
        })
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)