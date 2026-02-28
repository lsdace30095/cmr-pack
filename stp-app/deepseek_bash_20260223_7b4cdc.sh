cat <<EOF | kubectl apply -f -
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    # Let's Encrypt staging server - use for testing
    # server: https://acme-staging-v02.api.letsencrypt.org/directory
    # Production server - uncomment for real certificates
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your-email@example.com  # Change this to your email
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
EOF