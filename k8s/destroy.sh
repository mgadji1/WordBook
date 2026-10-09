#!/bin/bash
set -euo pipefail

echo "1. Deleting frontend..."
kubectl delete -k k8s/frontend --ignore-not-found

echo "2. Deleting backend..."
kubectl delete -k k8s/backend --ignore-not-found

echo "3. Deleting migration Job..."
kubectl delete -k k8s/migrate --ignore-not-found

echo "4. Deleting PostgreSQL..."
kubectl delete -k k8s/postgres --ignore-not-found

echo "5. Deleting PostgreSQL PVC..."
kubectl delete pvc postgres-pvc --ignore-not-found

echo "WordBook has been destroyed!"
