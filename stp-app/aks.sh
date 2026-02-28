#!/bin/bash

# Variables
RESOURCE_GROUP="your-resource-group"
AKS_CLUSTER="your-aks-cluster"
ACR_NAME="your-acr-name"
NAMESPACE="default"

# Set AKS context
echo "Setting AKS context..."
az aks get-credentials --resource-group $RESOURCE_GROUP --name $AKS_CLUSTER

# Create namespace if not exists
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# Build and push Docker image
echo "Building Docker image..."
docker build -t $ACR_NAME.azurecr.io/stp-app:latest .

echo "Pushing to ACR..."
az acr login --name $ACR_NAME
docker push $ACR_NAME.azurecr.io/stp-app:latest

# Update image in deployment
sed -i "s|\${ACR_NAME}|$ACR_NAME|g" deployment.yaml

# Apply Kubernetes configurations
echo "Deploying to AKS..."
kubectl apply -f configmap.yaml -n $NAMESPACE
kubectl apply -f deployment.yaml -n $NAMESPACE
kubectl apply -f service.yaml -n $NAMESPACE
kubectl apply -f hpa.yaml -n $NAMESPACE

# Check deployment status
kubectl rollout status deployment/stp-deployment -n $NAMESPACE

# Get service IP
kubectl get service stp-service -n $NAMESPACE

echo "Deployment completed successfully!"