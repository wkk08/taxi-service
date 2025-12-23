#!/usr/bin/env python3
"""
运行所有测试的脚本
"""
import sys
import os
import pytest


def main():
    """主函数"""
    # 添加项目根目录到Python路径
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.insert(0, project_root)

    print("🚕 开始运行出租车服务测试套件")
    print(f"📁 项目目录: {project_root}")
    print("=" * 50)

    # 运行测试
    test_dir = os.path.dirname(__file__)
    result = pytest.main([
        test_dir,
        '-v',  # 详细输出
        '--tb=short',  # 简短的错误回溯
        '--cov=src',  # 生成覆盖率报告
        '--cov-report=term',  # 在终端显示覆盖率
        '--cov-report=html:coverage_html'  # 生成HTML覆盖率报告
    ])

    print("=" * 50)

    if result == 0:
        print("✅ 所有测试通过!")
    else:
        print(f"❌ 测试失败，退出代码: {result}")

    return result


if __name__ == '__main__':
    sys.exit(main())