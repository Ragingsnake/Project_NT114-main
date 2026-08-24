#!/bin/bash
set -e

PROXY_URL="${HTTP_PROXY:-http://host.docker.internal:3128}"
PROXY_ARGS="--build-arg HTTP_PROXY=$PROXY_URL --build-arg HTTPS_PROXY=$PROXY_URL --build-arg http_proxy=$PROXY_URL --build-arg https_proxy=$PROXY_URL"

echo "=== Building FL Docker Images ==="
echo "Proxy: $PROXY_URL"
echo ""

# Build ZKP Node first (shares zkp-builder cache with client)
echo "[1/4] Building fl-zkp-node..."
docker build -f docker/Dockerfile.zkp_node -t ragingsnake/fl-zkp-node:latest $PROXY_ARGS .

# Build Client (reuses zkp-builder cache from above)
echo "[2/4] Building fl-client..."
docker build -f docker/Dockerfile.client -t ragingsnake/fl-client:latest $PROXY_ARGS .

# Build Server (simple, no node needed)
echo "[3/4] Building fl-server..."
docker build -f docker/Dockerfile.server -t ragingsnake/fl-server:latest $PROXY_ARGS .

# Build Blockchain
echo "[4/4] Building fl-blockchain..."
docker build -f docker/Dockerfile.blockchain -t ragingsnake/fl-blockchain:latest $PROXY_ARGS .

echo ""
echo "=== All images built successfully! ==="
docker images | grep ragingsnake/fl-
