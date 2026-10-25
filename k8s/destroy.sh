#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "1. Deleting frontend..."
kubectl delete -k k8s/frontend --ignore-not-found

echo "2. Deleting backend..."
kubectl delete -k k8s/backend --ignore-not-found

echo "3. Deleting migration Job..."
kubectl delete -k k8s/migrate --ignore-not-found

echo "4. Deleting log collector..."
kubectl delete -k k8s/log-collector --ignore-not-found

echo "5. Deleting Grafana..."
kubectl delete -k k8s/grafana --ignore-not-found

echo "6. Deleting VictoriaLogs..."
kubectl delete -k k8s/victoria-logs --ignore-not-found

echo "7. Deleting PostgreSQL..."
kubectl delete -k k8s/postgres --ignore-not-found

echo "8. Deleting VictoriaMetrics..."
helm uninstall vmsingle --ignore-not-found

echo "9. Deleting all PVCs..."
kubectl delete pvc --all --ignore-not-found

echo "WordBook has been destroyed!"
