#!/bin/bash
set -e

#############################################
# CONFIGURATION (EDIT THESE ONCE)
#############################################

RESOURCE_GROUP="stp-rg"
AKS_CLUSTER="cmr-aks"
ACR_NAME="dacecontainer"
IMAGE_NAME="smartcity"
NAMESPACE="smartcity"

BASE_DOMAIN="dace.ai"
SUBDOMAINS=("api" "pulse" "tv")

EMAIL="admin@dace-it.us"

#############################################
# AUTO VARIABLES (DO NOT EDIT)
#############################################

TIMESTAMP=$(date +%s)
IMAGE_TAG="$ACR_NAME.azurecr.io/$IMAGE_NAME:$TIMESTAMP"

echo "🚀 Starting SmartCity Multi-Subdomain Deployment..."

#############################################
# LOGIN & CONNECT
#############################################

echo "🔐 Logging into Azure..."
az account show > /dev/null 2>&1 || az login

echo "🔗 Connecting to AKS..."
az aks get-credentials \
  --resource-group $RESOURCE_GROUP \
  --name $AKS_CLUSTER \
  --overwrite-existing

#############################################
# BUILD & PUSH IMAGE
#############################################

echo "🐳 Building Docker image..."
az acr login --name $ACR_NAME

docker build -t $IMAGE_TAG .
docker push $IMAGE_TAG

#############################################
# CREATE NAMESPACE IF NOT EXISTS
#############################################

kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

#############################################
# CREATE SECRET (if not exists)
#############################################

kubectl create secret generic azure-secrets \
  --from-literal=AZURE_MAPS_KEY="$AZURE_MAPS_KEY" \
  --namespace $NAMESPACE \
  --dry-run=client -o yaml | kubectl apply -f -

#############################################
# DEPLOYMENT
#############################################

cat <<EOF | kubectl apply -n $NAMESPACE -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: smartcity-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: smartcity
  template:
    metadata:
      labels:
        app: smartcity
    spec:
      containers:
      - name: smartcity
        image: $IMAGE_TAG
        ports:
        - containerPort: 8000
        env:
        - name: AZURE_MAPS_KEY
          valueFrom:
            secretKeyRef:
              name: azure-secrets
              key: AZURE_MAPS_KEY
EOF

#############################################
# SERVICE
#############################################

cat <<EOF | kubectl apply -n $NAMESPACE -f -
apiVersion: v1
kind: Service
metadata:
  name: smartcity-service
spec:
  type: ClusterIP
  selector:
    app: smartcity
  ports:
  - port: 80
    targetPort: 8000
EOF

#############################################
# INSTALL INGRESS (if not installed)
#############################################

kubectl get ingressclass nginx > /dev/null 2>&1 || \
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml

#############################################
# INSTALL CERT-MANAGER (if not installed)
#############################################

kubectl get pods -n cert-manager > /dev/null 2>&1 || \
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/latest/download/cert-manager.yaml

sleep 20

#############################################
# CLUSTER ISSUER
#############################################

cat <<EOF | kubectl apply -f -
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: $EMAIL
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
EOF

#############################################
# INGRESS WITH MULTIPLE SUBDOMAINS
#############################################

TLS_HOSTS=""
RULES=""

for SUB in "${SUBDOMAINS[@]}"
do
  TLS_HOSTS="$TLS_HOSTS
  - $SUB.$BASE_DOMAIN"

  RULES="$RULES
  - host: $SUB.$BASE_DOMAIN
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: smartcity-service
            port:
              number: 80"
done

cat <<EOF | kubectl apply -n $NAMESPACE -f -
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: smartcity-ingress
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
  - hosts:$TLS_HOSTS
    secretName: smartcity-tls
  rules:$RULES
EOF

#############################################
# AUTOSCALER
#############################################

cat <<EOF | kubectl apply -n $NAMESPACE -f -
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: smartcity-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: smartcity-app
  minReplicas: 3
  maxReplicas: 12
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 65
EOF

#############################################
# WAIT FOR ROLLOUT
#############################################

echo "⏳ Waiting for deployment rollout..."
kubectl rollout status deployment/smartcity-app -n $NAMESPACE

#############################################
# GET PUBLIC IP
#############################################

echo "🌍 Fetching Public IP..."
INGRESS_IP=$(kubectl get svc ingress-nginx-controller -n ingress-nginx -o jsonpath="{.status.loadBalancer.ingress[0].ip}")

echo ""
echo "================================================"
echo "✅ DEPLOYMENT COMPLETE"
echo "================================================"
echo ""
echo "Point DNS A records to:"
echo "$INGRESS_IP"
echo ""

for SUB in "${SUBDOMAINS[@]}"
do
  echo "https://$SUB.$BASE_DOMAIN"
done

echo ""
echo "🚀 SmartCity Multi-Subdomain AKS Deployment Ready!"
