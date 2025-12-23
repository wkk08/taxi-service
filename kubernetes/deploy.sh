#!/bin/bash
# Kubernetes部署脚本

set -e  # 遇到错误时退出

echo "🚕 开始部署Taxi Service到Kubernetes..."

# 检查kubectl是否安装
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl未安装，请先安装kubectl"
    exit 1
fi

# 检查kubectl配置
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ kubectl无法连接到集群，请检查配置"
    exit 1
fi

echo "✅ 连接到Kubernetes集群: $(kubectl cluster-info | head -n1)"

# 创建命名空间（如果不存在）
echo "📁 创建命名空间..."
kubectl apply -f namespace.yaml

# 部署配置和密钥
echo "🔑 部署配置和密钥..."
kubectl apply -f configmap.yaml
kubectl apply -f secrets.yaml

# 部署数据库（可选）
read -p "是否部署数据库？(y/n): " deploy_db
if [[ $deploy_db == "y" || $deploy_db == "Y" ]]; then
    echo "🗄️ 部署数据库..."
    kubectl apply -f database.yaml
fi

# 部署Redis（可选）
read -p "是否部署Redis？(y/n): " deploy_redis
if [[ $deploy_redis == "y" || $deploy_redis == "Y" ]]; then
    echo "🧠 部署Redis..."
    kubectl apply -f redis.yaml
fi

# 部署主应用
echo "🚀 部署Taxi Service..."
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# 部署Ingress（可选）
read -p "是否部署Ingress？(y/n): " deploy_ingress
if [[ $deploy_ingress == "y" || $deploy_ingress == "Y" ]]; then
    echo "🌐 部署Ingress..."
    kubectl apply -f ingress.yaml
fi

# 部署HPA（可选）
read -p "是否部署自动扩缩容？(y/n): " deploy_hpa
if [[ $deploy_hpa == "y" || $deploy_hpa == "Y" ]]; then
    echo "📈 部署水平自动扩缩容..."
    kubectl apply -f hpa.yaml
fi

# 等待应用就绪
echo "⏳ 等待应用启动..."
kubectl wait --for=condition=available --timeout=300s deployment/taxi-service

# 显示部署状态
echo "📊 部署状态:"
kubectl get all -l app=taxi-service

echo "✅ 部署完成！"

# 显示访问信息
echo ""
echo "🌐 访问信息:"
echo "1. 集群内访问:"
echo "   kubectl port-forward svc/taxi-service 8080:80"
echo "   然后在浏览器访问: http://localhost:8080"
echo ""
echo "2. 服务地址:"
echo "   kubectl get svc taxi-service"
echo ""
echo "3. 查看日志:"
echo "   kubectl logs -f deployment/taxi-service"
echo ""
echo "4. 查看Pod状态:"
echo "   kubectl get pods -l app=taxi-service"