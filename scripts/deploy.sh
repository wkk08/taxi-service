#!/bin/bash

# 出租车服务部署脚本
# 使用方法: ./scripts/deploy.sh [environment]

set -e  # 遇到错误时退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_debug() {
    echo -e "${BLUE}[DEBUG]${NC} $1"
}

# 帮助信息
show_help() {
    echo "出租车服务部署脚本"
    echo ""
    echo "使用方法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -e, --environment ENV   部署环境 (development, staging, production)"
    echo "  -c, --config FILE       配置文件路径"
    echo "  -h, --help              显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 --environment production"
    echo "  $0 -e staging -c config/staging.env"
}

# 默认值
ENVIRONMENT="development"
CONFIG_FILE=""

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -e|--environment)
            ENVIRONMENT="$2"
            shift 2
            ;;
        -c|--config)
            CONFIG_FILE="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            log_error "未知选项: $1"
            show_help
            exit 1
            ;;
    esac
done

# 验证环境
validate_environment() {
    case $ENVIRONMENT in
        development|staging|production)
            log_info "部署环境: $ENVIRONMENT"
            ;;
        *)
            log_error "无效的环境: $ENVIRONMENT"
            log_error "有效环境: development, staging, production"
            exit 1
            ;;
    esac
}

# 加载配置
load_config() {
    if [[ -n "$CONFIG_FILE" && -f "$CONFIG_FILE" ]]; then
        log_info "加载配置文件: $CONFIG_FILE"
        source "$CONFIG_FILE"
    elif [[ -f ".env.$ENVIRONMENT" ]]; then
        log_info "加载环境配置文件: .env.$ENVIRONMENT"
        source ".env.$ENVIRONMENT"
    elif [[ -f ".env" ]]; then
        log_info "加载默认配置文件: .env"
        source ".env"
    else
        log_warn "未找到配置文件，使用默认值"
    fi
}

# 检查依赖
check_dependencies() {
    log_info "检查系统依赖..."

    # 检查Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker未安装"
        exit 1
    fi

    # 检查Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose未安装"
        exit 1
    fi

    log_info "Docker版本: $(docker --version)"
    log_info "Docker Compose版本: $(docker-compose --version)"

    # 检查Docker服务状态
    if ! docker info &> /dev/null; then
        log_error "Docker服务未运行"
        exit 1
    fi
}

# 构建Docker镜像
build_images() {
    log_info "构建Docker镜像..."

    # 设置构建参数
    BUILD_ARGS=""
    if [[ "$ENVIRONMENT" == "production" ]]; then
        BUILD_ARGS="--no-cache"
    fi

    # 构建镜像
    docker-compose build $BUILD_ARGS

    if [[ $? -eq 0 ]]; then
        log_info "Docker镜像构建成功"
    else
        log_error "Docker镜像构建失败"
        exit 1
    fi
}

# 运行数据库迁移
run_migrations() {
    log_info "运行数据库迁移..."

    # 等待数据库服务启动
    log_info "等待数据库服务就绪..."
    sleep 10

    # 运行迁移
    docker-compose run --rm web python scripts/migrate.py

    if [[ $? -eq 0 ]]; then
        log_info "数据库迁移成功"
    else
        log_error "数据库迁移失败"
        exit 1
    fi
}

# 启动服务
start_services() {
    log_info "启动服务..."

    # 停止并移除旧容器
    log_info "清理旧容器..."
    docker-compose down --remove-orphans

    # 启动新容器
    if [[ "$ENVIRONMENT" == "production" ]]; then
        docker-compose up -d --scale web=3
    else
        docker-compose up -d
    fi

    if [[ $? -eq 0 ]]; then
        log_info "服务启动成功"
    else
        log_error "服务启动失败"
        exit 1
    fi
}

# 运行测试
run_tests() {
    if [[ "$ENVIRONMENT" != "production" ]]; then
        log_info "运行测试..."

        # 等待应用启动
        log_info "等待应用启动..."
        sleep 15

        # 运行测试
        docker-compose exec -T web pytest tests/ -v

        if [[ $? -eq 0 ]]; then
            log_info "测试通过"
        else
            log_error "测试失败"
            # 在开发环境中，测试失败不中断部署
            if [[ "$ENVIRONMENT" == "production" ]]; then
                exit 1
            fi
        fi
    fi
}

# 验证部署
verify_deployment() {
    log_info "验证部署..."

    # 等待服务完全启动
    sleep 10

    # 获取服务URL
    if [[ "$ENVIRONMENT" == "production" ]]; then
        SERVICE_URL="http://localhost"
    else
        SERVICE_URL="http://localhost:5000"
    fi

    # 检查健康端点
    log_info "检查健康状态..."
    HEALTH_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$SERVICE_URL/health" || echo "000")

    if [[ "$HEALTH_RESPONSE" == "200" ]]; then
        log_info "健康检查通过"
    else
        log_error "健康检查失败 (HTTP $HEALTH_RESPONSE)"
        # 显示容器状态和日志
        docker-compose ps
        docker-compose logs --tail=50 web
        exit 1
    fi

    # 检查API端点
    log_info "检查API端点..."
    API_RESPONSE=$(curl -s "$SERVICE_URL/" || echo "{}")

    if echo "$API_RESPONSE" | grep -q "Taxi Service API"; then
        log_info "API端点正常"
    else
        log_error "API端点异常"
        log_debug "响应: $API_RESPONSE"
        exit 1
    fi
}

# 显示部署信息
show_deployment_info() {
    log_info "========== 部署完成 =========="
    log_info "环境: $ENVIRONMENT"
    log_info "时间: $(date)"

    # 显示服务信息
    log_info "服务状态:"
    docker-compose ps

    # 显示访问信息
    if [[ "$ENVIRONMENT" == "production" ]]; then
        log_info "访问地址: http://your-domain.com"
    else
        log_info "访问地址: http://localhost:5000"
        log_info "API文档: http://localhost:5000/"
    fi

    log_info "健康检查: http://localhost:5000/health"
    log_info "查看日志: docker-compose logs -f"
    log_info "停止服务: docker-compose down"
    log_info "=================================="
}

# 主部署流程
main() {
    log_info "开始部署出租车服务..."

    # 验证环境
    validate_environment

    # 加载配置
    load_config

    # 检查依赖
    check_dependencies

    # 构建镜像
    build_images

    # 运行迁移
    run_migrations

    # 启动服务
    start_services

    # 运行测试
    run_tests

    # 验证部署
    verify_deployment

    # 显示部署信息
    show_deployment_info

    log_info "部署成功完成！"
}

# 执行主函数
main "$@"