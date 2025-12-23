#!/usr/bin/env python3
"""
最小化启动脚本 - 绕过所有导入问题
"""
import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask

# 创建最简单的Flask应用
app = Flask(__name__)


@app.route('/')
def home():
    return "🚕 Taxi Service API is running!"


@app.route('/health')
def health():
    return {
        "status": "healthy",
        "service": "taxi-service",
        "message": "Minimal version is working"
    }


if __name__ == '__main__':
    print("🚕 Starting Taxi Service (Minimal Version)...")
    print(f"📂 Project directory: {os.getcwd()}")
    print(f"🐍 Python path: {sys.path}")
    print("🌐 Server will start at: http://localhost:5000")

    app.run(host='0.0.0.0', port=5000, debug=True)