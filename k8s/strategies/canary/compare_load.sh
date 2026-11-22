#!/bin/bash

v1=0
v2=0

for i in {1..100}; do
    GATEWAY_IP=$(kubectl get gateway wordbook-gateway -o jsonpath='{.status.addresses[0].value}')
    response=$(curl -s "http://$GATEWAY_IP/")

    if [[ "$response" == *'"version":"1.0"'* ]]; then
        ((v1++))
    elif [[ "$response" == *'"version":"2.0"'* ]]; then
        ((v2++))
    fi
done

echo "Version 1.0: $v1"
echo "Version 2.0: $v2"
echo "Total: $((v1 + v2))"