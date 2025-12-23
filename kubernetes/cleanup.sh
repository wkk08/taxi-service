#!/bin/bash
# 清理Kubernetes部署

set -e

echo "🧹 开始清理Taxi Service部署..."

# 删除所有资源
kubectl delete deployment taxi-service --ignore-not-found
kubectl delete service taxi-service --ignore-not-found
kubectl delete ingress taxi-ingress --ignore-not-found
kubectl delete hpa taxi-service-hpa --ignore-not-found

# 删除数据库（可选）
read -p "是否删除数据库？(y/n): " delete_db
if [[ $delete_db == "y" || $delete_db == "Y" ]]; then
    kubectl delete statefulset postgres --ignore-not-found
    kubectl delete service postgres --ignore-not-found
    kubectl delete pvc postgres-pvc --ignore-not-found
fi

# 删除Redis（可选）
read -p "是否删除Redis？(y/n): " delete_redis
if [[ $delete_redis == "y" || $delete_redis == "Y" ]]; then
    kubectl delete deployment redis --ignore-not-found
    kubectl delete service redis --ignore-not-found
    kubectl delete configmap redis-config --ignore-not-found
    kubectl delete pvc redis-pvc --ignore-not-found
fi

# 删除配置
kubectl delete configmap taxi-config --ignore-not-found
kubectl delete secret taxi-secrets --ignore-not-found

# 删除命名空间（如果使用了独立的命名空间）
# kubectl delete namespace taxi-namespace --ignore-not-found

echo "✅ 清理完成！"