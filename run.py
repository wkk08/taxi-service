#!/usr/bin/env python3
"""
Taxi Service - 启动脚本
"""
import sys
import os

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print(f"🚕 Taxi Service - Starting...")
print(f"📁 Project directory: {current_dir}")

try:
    # 导入并运行应用
    from src.app import app

    if __name__ == '__main__':
        # 获取端口，默认为5000
        port = int(os.environ.get('PORT', 5000))

        # 获取调试模式
        debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'

        print("=" * 50)
        print(f"🌐 Server: http://localhost:{port}")
        print(f"🐞 Debug mode: {debug}")
        print("=" * 50)

        # 运行应用
        app.run(host='0.0.0.0', port=port, debug=debug)

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("\nTrying alternative import...")

    # 尝试直接运行Flask应用
    try:
        # 设置环境变量
        os.environ['FLASK_APP'] = 'src/app.py'

        # 使用Flask命令行运行
        from flask import Flask

        app = Flask(__name__)


        @app.route('/')
        def home():
            return "🚕 Taxi Service - Alternative Start"


        port = 5000
        print(f"Starting alternative server on port {port}")
        app.run(port=port, debug=True)

    except Exception as e2:
        print(f"❌ Failed to start: {e2}")
        sys.exit(1)