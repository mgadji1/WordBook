#!/bin/bash
set -euo pipefail

echo "1. Deploying PostgreSQL..."
kubectl apply -k k8s/postgres
kubectl rollout status statefulset/postgres --timeout=60s

echo "2. Deploying backend secret..."
kubectl apply -f k8s/backend/secret.yaml

echo "3. Running database migrations..."
kubectl delete job migrate --ignore-not-found
kubectl apply -k k8s/migrate
kubectl wait --for=condition=complete job/migrate --timeout=60s

echo "4. Deploying backend..."
kubectl apply -k k8s/backend
kubectl rollout status deployment/backend --timeout=60s

echo "5. Deploying frontend..."
kubectl apply -k k8s/frontend
kubectl rollout status deployment/frontend --timeout=60s

echo "Successful deployment!"
