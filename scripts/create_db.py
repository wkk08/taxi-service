#!/usr/bin/env python3
"""
创建数据库表的简单脚本
"""

import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# 首先创建 Flask 应用并配置数据库
from flask import Flask


def create_app():
    """创建 Flask 应用"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taxi.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev-secret-key'
    return app


def create_database():
    """创建数据库表"""
    print("=" * 50)
    print("创建出租车服务数据库")
    print("=" * 50)

    try:
        # 创建应用
        app = create_app()

        # 初始化数据库
        from src.services.database import db
        db.init_app(app)

        with app.app_context():
            # 导入所有模型以确保它们被注册
            print("导入模型...")
            from src.models.user import User
            from src.models.ride import Ride
            from src.models.vehicle import Vehicle

            # 创建所有表
            print("创建数据库表...")
            db.create_all()

            print("✓ 数据库表创建成功")

            # 插入一些测试数据
            print("插入测试数据...")
            insert_test_data(db)

            print("✓ 测试数据插入成功")

        print("\n" + "=" * 50)
        print("数据库创建完成！")
        print("数据库文件: taxi.db")
        print("=" * 50)

        return True

    except Exception as e:
        print(f"\n❌ 数据库创建失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def insert_test_data(db):
    """插入测试数据"""
    from werkzeug.security import generate_password_hash
    import datetime

    # 检查是否已有数据
    from src.models.user import User
    if User.query.count() > 0:
        print("数据库中已有数据，跳过测试数据插入")
        return

    # 1. 创建车辆
    from src.models.vehicle import Vehicle
    vehicles = [
        Vehicle(
            make="Toyota",
            model="Camry",
            year=2022,
            color="Silver",
            license_plate="TAXI001",
            vehicle_type="sedan",
            capacity=4,
            fuel_type="hybrid",
            transmission="automatic"
        ),
        Vehicle(
            make="Honda",
            model="Accord",
            year=2021,
            color="Black",
            license_plate="TAXI002",
            vehicle_type="sedan",
            capacity=4,
            fuel_type="gasoline",
            transmission="automatic"
        ),
        Vehicle(
            make="Ford",
            model="Explorer",
            year=2023,
            color="White",
            license_plate="TAXI003",
            vehicle_type="suv",
            capacity=6,
            fuel_type="gasoline",
            transmission="automatic"
        )
    ]

    for vehicle in vehicles:
        db.session.add(vehicle)

    db.session.commit()
    print(f"  创建了 {len(vehicles)} 辆测试车辆")

    # 2. 创建用户
    users = [
        # 乘客
        User(
            email="alice@example.com",
            username="alice",
            password_hash=generate_password_hash("password123"),
            role="passenger",
            phone="+12345678901"
        ),
        User(
            email="bob@example.com",
            username="bob",
            password_hash=generate_password_hash("password123"),
            role="passenger",
            phone="+12345678902"
        ),
        # 司机
        User(
            email="charlie@example.com",
            username="charlie_driver",
            password_hash=generate_password_hash("password123"),
            role="driver",
            phone="+12345678903",
            driver_id="DRV001",
            license_number="LIC001",
            vehicle_id=1,
            current_location="40.7128,-74.0060",
            is_available=True,
            rating=4.8
        ),
        User(
            email="diana@example.com",
            username="diana_driver",
            password_hash=generate_password_hash("password123"),
            role="driver",
            phone="+12345678904",
            driver_id="DRV002",
            license_number="LIC002",
            vehicle_id=2,
            current_location="40.7589,-73.9851",
            is_available=True,
            rating=4.9
        )
    ]

    for user in users:
        db.session.add(user)

    db.session.commit()
    print(f"  创建了 {len(users)} 个测试用户")

    # 3. 创建行程
    from src.models.ride import Ride
    rides = [
        Ride(
            passenger_id=1,  # alice
            driver_id=3,  # charlie
            pickup_address="123 Main St, New York, NY",
            dropoff_address="456 Broadway, New York, NY",
            pickup_lat=40.7128,
            pickup_lng=-74.0060,
            dropoff_lat=40.7589,
            dropoff_lng=-73.9851,
            status="completed",
            requested_at=datetime.datetime.utcnow() - datetime.timedelta(days=2),
            accepted_at=datetime.datetime.utcnow() - datetime.timedelta(days=2, minutes=2),
            started_at=datetime.datetime.utcnow() - datetime.timedelta(days=2, minutes=5),
            completed_at=datetime.datetime.utcnow() - datetime.timedelta(days=2, minutes=25),
            estimated_fare=15.50,
            actual_fare=16.25,
            payment_status="paid",
            passenger_rating=5,
            driver_rating=5
        ),
        Ride(
            passenger_id=2,  # bob
            driver_id=4,  # diana
            pickup_address="789 Park Ave, New York, NY",
            dropoff_address="321 5th Ave, New York, NY",
            pickup_lat=40.7749,
            pickup_lng=-73.9654,
            dropoff_lat=40.7489,
            dropoff_lng=-73.9680,
            status="in_progress",
            requested_at=datetime.datetime.utcnow() - datetime.timedelta(minutes=10),
            accepted_at=datetime.datetime.utcnow() - datetime.timedelta(minutes=8),
            started_at=datetime.datetime.utcnow() - datetime.timedelta(minutes=5),
            estimated_fare=12.75
        ),
        Ride(
            passenger_id=1,  # alice
            pickup_address="555 Central Park West, New York, NY",
            dropoff_address="999 Times Square, New York, NY",
            pickup_lat=40.7851,
            pickup_lng=-73.9683,
            dropoff_lat=40.7580,
            dropoff_lng=-73.9855,
            status="requested",
            requested_at=datetime.datetime.utcnow() - datetime.timedelta(minutes=2),
            estimated_fare=18.25
        )
    ]

    for ride in rides:
        db.session.add(ride)

    db.session.commit()
    print(f"  创建了 {len(rides)} 个测试行程")


if __name__ == "__main__":
    success = create_database()
    sys.exit(0 if success else 1)