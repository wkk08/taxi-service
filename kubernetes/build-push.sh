#!/bin/bash
# 构建和推送Docker镜像

set -e

echo "🐳 开始构建和推送Taxi Service镜像..."

# 设置变量
IMAGE_NAME="ghcr.io/YOUR_USERNAME/taxi-service"
IMAGE_TAG=$(git rev-parse --short HEAD)
LATEST_TAG="latest"

# 登录到GitHub Container Registry
echo "🔐 登录到GitHub Container Registry..."
echo "$GITHUB_TOKEN" | docker login ghcr.io -u YOUR_USERNAME --password-stdin

# 构建镜像
echo "🔨 构建Docker镜像..."
docker build -t $IMAGE_NAME:$IMAGE_TAG -t $IMAGE_NAME:$LATEST_TAG .

# 推送镜像
echo "🚀 推送镜像到GitHub Container Registry..."
docker push $IMAGE_NAME:$IMAGE_TAG
docker push $IMAGE_NAME:$LATEST_TAG

echo "✅ 镜像构建和推送完成！"
echo ""
echo "📦 镜像信息:"
echo "   标签: $IMAGE_NAME:$IMAGE_TAG"
echo "   最新: $IMAGE_NAME:$LATEST_TAG"