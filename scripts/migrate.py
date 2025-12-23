#!/usr/bin/env python3
"""
数据库迁移脚本
用于创建数据库表和应用初始数据
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.app import create_app
from src.services.database import db, init_db
from src.models.user import User
from src.models.ride import Ride
from src.models.vehicle import Vehicle
import datetime


def create_tables():
    """创建数据库表"""
    print("创建数据库表...")

    app = create_app()
    with app.app_context():
        # 初始化数据库
        init_db(app)
        print("✓ 数据库表创建完成")


def seed_initial_data():
    """插入初始数据"""
    print("插入初始数据...")

    app = create_app()
    with app.app_context():
        # 检查是否已有数据
        user_count = User.query.count()
        if user_count > 0:
            print("✓ 数据库中已有数据，跳过初始数据插入")
            return

        # 创建示例车辆
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
        print(f"✓ 创建了 {len(vehicles)} 辆示例车辆")

        # 创建示例用户（乘客和司机）
        from werkzeug.security import generate_password_hash

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
        print(f"✓ 创建了 {len(users)} 个示例用户")

        # 创建示例行程
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
        print(f"✓ 创建了 {len(rides)} 个示例行程")


def main():
    """主函数"""
    print("=" * 50)
    print("出租车服务数据库迁移工具")
    print("=" * 50)

    try:
        # 创建表
        create_tables()

        # 插入初始数据
        seed_initial_data()

        print("\n" + "=" * 50)
        print("数据库迁移完成！")
        print("=" * 50)

    except Exception as e:
        print(f"\n❌ 数据库迁移失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()