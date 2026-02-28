#!/bin/bash

echo "🔧 Fixing ClusterIssuer with valid email"

# Step 1: Delete existing ClusterIssuer
echo "📝 Removing old ClusterIssuer..."
kubectl delete clusterissuer letsencrypt-prod --ignore-not-found

# Step 2: Create new ClusterIssuer with valid email
echo "📝 Creating new ClusterIssuer with valid email..."
read -p "Enter your email address for Let's Encrypt: " EMAIL
cat <<EOF | kubectl apply -f -
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: admin@dace-it.us
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
EOF

# Step 3: Verify ClusterIssuer is ready
echo "⏳ Waiting for ClusterIssuer to be ready..."
sleep 5
kubectl get clusterissuer letsencrypt-prod

# Step 4: Clean up old certificate resources
echo "📝 Cleaning up old certificate resources..."
kubectl delete certificate stp-tls-secret --ignore-not-found
kubectl delete secret stp-tls-secret --ignore-not-found
kubectl delete certificaterequest -l cert-manager.io/certificate-name=stp-tls-secret --ignore-not-found

# Step 5: Fix ingress annotations
echo "🏷️  Fixing ingress annotations..."
kubectl annotate ingress stp-ingress cert-manager.io/issuer- cert-manager.io/cluster-issuer- --overwrite
kubectl annotate ingress stp-ingress cert-manager.io/cluster-issuer=letsencrypt-prod --overwrite

# Step 6: Watch certificate creation
echo "👀 Watching certificate creation (press Ctrl+C to stop watching)..."
kubectl get certificate -w &

# Step 7: Check if certificate is created
sleep 10
echo -e "\n📊 Current certificate status:"
kubectl get certificate

# Step 8: Check if secret is created
echo -e "\n🔑 Secret status:"
kubectl get secret stp-tls-secret 2>/dev/null || echo "Secret not created yet"

# Step 9: Restart ingress controller
echo -e "\n🔄 Restarting ingress controller..."
kubectl rollout restart deployment -n ingress-nginx ingress-nginx-controller
kubectl rollout status deployment -n ingress-nginx ingress-nginx-controller

# Step 10: Final status
echo -e "\n✅ Fix completed!"
echo "Check certificate status with: kubectl get certificate -w"
echo "Check secret with: kubectl get secret stp-tls-secret"
