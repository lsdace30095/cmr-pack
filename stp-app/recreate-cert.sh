#!/bin/bash

echo "🔧 Recreating SSL Certificate for stp-app"

# Step 1: Delete any existing certificate and secret
echo "📝 Cleaning up old resources..."
kubectl delete certificate stp-tls-secret --ignore-not-found
kubectl delete secret stp-tls-secret --ignore-not-found

# Step 2: Create new certificate
echo "📝 Creating new certificate..."
cat <<EOF | kubectl apply -f -
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: stp-tls-secret
  namespace: default
spec:
  secretName: stp-tls-secret
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
  dnsNames:
  - stp-app.dace.ai
  - stp-app.sensetrafficpulse.com
EOF

# Step 3: Wait for certificate to be ready
echo "⏳ Waiting for certificate to be issued (this may take a minute)..."
sleep 10

# Step 4: Check certificate status
echo "📊 Certificate status:"
kubectl get certificate stp-tls-secret

# Step 5: Wait for secret to be created
echo "⏳ Waiting for secret to be created..."
for i in {1..30}; do
    if kubectl get secret stp-tls-secret &>/dev/null; then
        echo "✅ Secret created!"
        break
    fi
    echo -n "."
    sleep 2
done
echo

# Step 6: Verify secret
if kubectl get secret stp-tls-secret &>/dev/null; then
    echo "✅ Secret type: $(kubectl get secret stp-tls-secret -o jsonpath='{.type}')"
else
    echo "❌ Secret not created yet. Check cert-manager logs:"
    kubectl logs -n cert-manager -l app=cert-manager --tail=20
    exit 1
fi

# Step 7: Restart ingress controller
echo "🔄 Restarting ingress controller..."
kubectl rollout restart deployment -n ingress-nginx ingress-nginx-controller
kubectl rollout status deployment -n ingress-nginx ingress-nginx-controller

# Step 8: Wait for ingress controller to pick up the secret
echo "⏳ Waiting for ingress controller to sync..."
sleep 10

# Step 9: Check if errors are gone
echo "🔍 Checking ingress controller logs for certificate errors:"
ERRORS=$(kubectl logs -n ingress-nginx -l app.kubernetes.io/component=controller --tail=20 2>/dev/null | grep -i "certificate.*not found" || echo "✅ No certificate errors found!")
echo "$ERRORS"

# Step 10: Test endpoints
echo -e "\n🌐 Testing endpoints:"
for domain in stp-app.dace.ai stp-app.sensetrafficpulse.com; do
    echo "=== $domain ==="
    echo -n "HTTP -> HTTPS: "
    curl -I -s http://$domain/health 2>/dev/null | head -n 1
    echo -n "HTTPS: "
    curl -I -s https://$domain/health 2>/dev/null | head -n 1
    echo
done

echo "✅ Fix complete!"
