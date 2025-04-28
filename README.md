# FastAPI RAG + Auth API on Azure Kubernetes Service (AKS)

This project is a **FastAPI-based RAG + Auth API** with robust authentication, async DB migrations (Alembic), secure secret management, and production-ready deployment on Azure Kubernetes Service (AKS).

---

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Setup](#setup)
  - [Azure Resource Preparation](#azure-resource-preparation)
  - [Build and Push Docker Image](#build-and-push-docker-image)
  - [Configure and Attach Azure Container Registry](#configure-and-attach-azure-container-registry)
  - [AKS Cluster and NGINX Ingress](#aks-cluster-and-nginx-ingress)
  - [Secrets & Environment Variables](#secrets--environment-variables)
  - [Deployment with Helm](#deployment-with-helm)
  - [DNS Setup](#dns-setup)
  - [Database Migrations (Alembic)](#database-migrations-alembic)
- [Usage](#usage)
- [Best Practices & Security](#best-practices--security)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

- Python 3.11
- Docker
- Azure CLI
- kubectl
- Helm
- Azure Subscription with AKS and ACR permissions
- A domain/subdomain you can manage

---

## Project Structure

```
project-root/
├── Dockerfile
├── requirements.txt
├── alembic.ini
├── alembic/
│   ├── env.py
│   └── versions/
├── src/
│   └── app/
│       ├── main.py
│       └── ...
└── helm/
    └── rag-api/
        ├── templates/
        │   ├── deployment.yaml
        │   ├── service.yaml
        │   ├── ingress.yaml
        │   └── alembic-job.yaml
        └── values.yaml
```

---

## Setup

### Azure Resource Preparation

```sh
az group create --name my-aks-rg --location eastus
az acr create --resource-group my-aks-rg --name myacrregistry --sku Basic
```

### Build and Push Docker Image

```sh
az acr login --name myacrregistry
docker build -t myacrregistry.azurecr.io/rag-api:latest .
docker push myacrregistry.azurecr.io/rag-api:latest
```

### Configure and Attach Azure Container Registry

```sh
az aks create     --resource-group my-aks-rg     --name my-aks-cluster     --node-count 3     --generate-ssh-keys     --attach-acr myacrregistry

az aks get-credentials --resource-group my-aks-rg --name my-aks-cluster
```

### AKS Cluster and NGINX Ingress

```sh
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
kubectl create namespace ingress

helm install nginx-ingress ingress-nginx/ingress-nginx     --namespace ingress     --set controller.service.type=LoadBalancer     --set controller.service.externalTrafficPolicy=Local

kubectl get svc -n ingress -w  # Wait for EXTERNAL-IP to appear
```

### Secrets & Environment Variables

```sh
kubectl create namespace rag

kubectl create secret generic rag-api-secret   --from-literal=DATABASE_URL="postgresql+asyncpg://postgres:YOURPW@az-postgres-host:5432/YOURDB"   --from-literal=OPENAI_API_KEY="sk-..."   --from-literal=SECRET_KEY="changeme-supersecret"   --from-literal=USER_SALT="changeme-pepper"   --namespace rag
```

### Deployment with Helm

1. Edit `helm/rag-api/values.yaml` with your image, env, and ingress config.
2. Deploy with:
   ```sh
   helm upgrade --install rag-api ./helm/rag-api      --namespace rag      --set image.repository=myacrregistry.azurecr.io/rag-api      --set image.tag=latest
   ```

### DNS Setup

- Add an A record in your DNS provider or Azure DNS:
  ```
  api.example.com → <your-ingress EXTERNAL-IP>
  ```

### Database Migrations (Alembic)

Create a Kubernetes Job (`alembic-job.yaml`):

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: alembic-upgrade
  namespace: rag
spec:
  template:
    spec:
      restartPolicy: Never
      containers:
      - name: migrate
        image: myacrregistry.azurecr.io/rag-api:latest
        command: ["alembic", "upgrade", "head"]
        envFrom:
          - secretRef:
              name: rag-api-secret
        env:
          - name: PYTHONPATH
            value: /app/src
```

Apply and check logs:
```sh
kubectl apply -f helm/rag-api/templates/alembic-job.yaml
kubectl logs job/alembic-upgrade -n rag
```

To rerun:
```sh
kubectl delete job alembic-upgrade -n rag
kubectl apply -f helm/rag-api/templates/alembic-job.yaml
```

---

## Usage

- API docs: `http://api.example.com/docs`
- **Obtain a JWT**:
  ```python
  import requests
  url = "http://api.example.com/token"
  data = {"username": "your_email", "password": "your_password"}
  r = requests.post(url, data=data)
  print("Token:", r.json())
  ```
- **Call Protected Endpoint**:
  ```python
  headers = {"Authorization": f"Bearer {token}"}
  r = requests.get("http://api.example.com/users/me", headers=headers)
  print(r.json())
  ```

---

## Best Practices & Security

- Use HTTPS on Ingress for all non-local/prod endpoints.
- Restrict ingress: Use Azure NSGs or K8s NetworkPolicy if appropriate.
- Never commit secrets to git; always use K8s Secrets.
- Monitor with Azure Log Analytics and AKS built-in monitoring.
- Keep Alembic migrations in `alembic/versions/` and run migrations only via Job, not inside the app container.

---

## Troubleshooting

- **Alembic migration fails**:
  - Ensure `alembic.ini` and `alembic/` are in `/app`, image rebuilt and pushed.
  - Verify environment variables are loaded from K8s Secret.
- **External access fails**:
  - Check Ingress EXTERNAL-IP.
  - Ensure Load Balancer health probe is healthy (HTTP 200 on `/`).
  - Check DNS propagation.
- **Python import errors**:
  - Use `from app...` in Alembic `env.py` if `PYTHONPATH=/app/src`.
