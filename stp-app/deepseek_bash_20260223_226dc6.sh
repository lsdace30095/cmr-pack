#!/bin/bash

echo "🔧 Fixing Docker image with application code..."

# Ensure directories exist
mkdir -p core_pla_2049_engine/optical_flow_adapters
mkdir -p core_pla_2049_engine/vector_processing
mkdir -p core_pla_2049_engine/coherent_regions
mkdir -p core_pla_2049_engine/region_graphs

# Create __init__.py files
touch core_pla_2049_engine/__init__.py
touch core_pla_2049_engine/optical_flow_adapters/__init__.py
touch core_pla_2049_engine/vector_processing/__init__.py
touch core_pla_2049_engine/coherent_regions/__init__.py
touch core_pla_2049_engine/region_graphs/__init__.py

# Check if main.py exists
if [ ! -f main.py ]; then
    echo "❌ main.py not found! Please ensure main.py is in the current directory."
    exit 1
fi

# Rebuild Docker image
echo "🐳 Building Docker image..."
docker build -t stpcontainerregistry2026.azurecr.io/stp-app:latest .

# Push to ACR
echo "📤 Pushing to ACR..."
az acr login --name stpcontainerregistry2026
docker push stpcontainerregistry2026.azurecr.io/stp-app:latest

# Restart deployment
echo "🔄 Restarting AKS deployment..."
kubectl rollout restart deployment/stp-deployment

# Wait for rollout
echo "⏳ Waiting for rollout to complete..."
kubectl rollout status deployment/stp-deployment

# Check pods
echo "📊 Current pods:"
kubectl get pods

echo "✅ Fix applied! Check logs with: kubectl logs -f deployment/stp-deployment"