#!/bin/bash

# Variables
RESOURCE_GROUP="stp-rg"
LOCATION="eastus"
AKS_NAME="cmr-aks"
ACR_NAME="stpcontainerregistry2026"  # Added year to make it more unique

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}Step 1: Creating Resource Group...${NC}"
az group create --name $RESOURCE_GROUP --location $LOCATION
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to create resource group${NC}"
    exit 1
fi

echo -e "${GREEN}Step 2: Creating Azure Container Registry...${NC}"
az acr create \
  --resource-group $RESOURCE_GROUP \
  --name $ACR_NAME \
  --sku Basic \
  --admin-enabled true
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to create ACR. Try a different name for ACR_NAME${NC}"
    exit 1
fi

echo -e "${GREEN}Step 3: Creating AKS Cluster...${NC}"
az aks create \
  --resource-group $RESOURCE_GROUP \
  --name $AKS_NAME \
  --node-count 3 \
  --enable-addons monitoring \
  --generate-ssh-keys \
  --node-vm-size Standard_DS2_v2 \
  --attach-acr $ACR_NAME
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to create AKS cluster${NC}"
    exit 1
fi

echo -e "${GREEN}Step 4: Getting AKS credentials...${NC}"
az aks get-credentials --resource-group $RESOURCE_GROUP --name $AKS_NAME --overwrite-existing

echo -e "${GREEN}Step 5: Verifying cluster access...${NC}"
kubectl get nodes

echo -e "${GREEN}Setup completed successfully!${NC}"
echo -e "Resource Group: $RESOURCE_GROUP"
echo -e "AKS Cluster: $AKS_NAME"
echo -e "ACR: $ACR_NAME"
