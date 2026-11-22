#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "1. Deleting HTTPRoute..."
kubectl delete -f k8s/gateway/backend-route.yaml --ignore-not-found

echo "2. Deleting Gateway..."
kubectl delete -f k8s/gateway/gateway.yaml --ignore-not-found

echo "3. Deleting GatewayClass..."
kubectl delete -f k8s/gateway/gateway-class.yaml --ignore-not-found

echo "4. Uninstalling Envoy Gateway..."
helm uninstall eg -n envoy-gateway-system --ignore-not-found

kubectl delete namespace envoy-gateway-system --ignore-not-found --wait=false

echo "5. Deleting prober..."
kubectl delete -k k8s/prober --ignore-not-found

echo "6. Deleting alerting..."
kubectl delete -k k8s/alerting --ignore-not-found

echo "7. Deleting frontend..."
kubectl delete -k k8s/frontend --ignore-not-found

echo "8. Deleting backend..."
kubectl delete -k k8s/backend --ignore-not-found

echo "9. Deleting migration Job..."
kubectl delete -k k8s/migrate --ignore-not-found

echo "10. Deleting log collector..."
kubectl delete -k k8s/log-collector --ignore-not-found

echo "11. Deleting Grafana..."
kubectl delete -k k8s/grafana --ignore-not-found

echo "12. Deleting VictoriaLogs..."
kubectl delete -k k8s/victoria-logs --ignore-not-found

echo "13. Deleting PostgreSQL..."
kubectl delete -k k8s/postgres --ignore-not-found

echo "14. Deleting VictoriaMetrics..."
helm uninstall vmsingle --ignore-not-found

echo "15. Deleting strategies containers..."
kubectl delete -k k8s/strategies/blue-green --ignore-not-found

echo "WordBook has been destroyed!"
