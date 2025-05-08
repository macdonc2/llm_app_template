# RAG + Auth API

## Deepwiki
Learn interactively with the codebase using Deepwiki!

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/macdonc2/llm_app_template)



## Overview

This repository provides a FastAPI service supporting:

- User registration & JWT-based authentication
- Retrieval-Augmented Generation (RAG) endpoint powered by OpenAI
- Clean architecture with Dependency Injection, Registry, Ports & Adapters, Services, and Routers
- Asynchronous PostgreSQL access via SQLAlchemy and Alembic migrations
- Dockerized build & VS Code Dev Container setup
- Kubernetes deployment on Azure AKS using Helm charts

---

## Repository Structure

```text
base_app/
├── .devcontainer/                # VS Code Remote Container config
│   ├── devcontainer.json
│   └── Dockerfile
├── .env                          # Environment variables (credentials & settings)
├── alembic.ini                   # Alembic configuration
├── alembic/                      # Database migrations
│   ├── env.py
│   └── versions/
│       ├── .empty
│       ├── 20250429_create_users_table.py
│       └── 20250429_add_openai_key.py
├── docker/                       # Production Docker image
│   └── Dockerfile
├── helm/                         # Helm charts for Kubernetes deployment
│   ├── cert-infra/               # cert-manager ClusterIssuer chart
│   │   ├── Chart.yaml
│   │   └── templates/
│   │       └── cluster-issuer-macdonml.yaml
│   └── rag-api/                  # RAG API application chart
│       ├── Chart.yaml
│       ├── values.yaml
│       ├── app-secrets.yaml      # Kubernetes Secret manifest template
│       └── templates/
│           ├── alembic-job.yaml
│           ├── deployment.yaml
│           ├── ingress.yaml
│           └── service.yaml
├── requirements.txt              # Python dependencies
└── src/
    └── app/                     # Application source code
        ├── main.py              # FastAPI app entrypoint
        ├── config.py            # Pydantic Settings for env vars
        ├── db.py                # SQLAlchemy Async engine & session
        ├── dependencies.py      # FastAPI dependency providers
        ├── registry.py          # Maps provider names to adapter classes
        ├── models.py            # SQLAlchemy ORM models
        ├── schemas.py           # Pydantic schemas for I/O
        ├── security.py          # JWT auth & password hashing
        ├── utils.py             # Helper functions (salt, ID generation)
        ├── adapters/            # Infrastructure implementations
        │   ├── openai_llm_adapter.py
        │   ├── openai_embedding_adapter.py
        │   └── postgres_user_repository.py
        ├── ports/               # Abstract base classes (Ports)
        │   ├── llm_port.py
        │   ├── embedding_port.py
        │   └── user_repository_port.py
        ├── services/            # Business logic
        │   ├── user_service.py
        │   ├── llm_service.py
        │   └── retrieval_service.py
        └── routers/             # HTTP endpoints
            ├── auth.py          # /token
            ├── users.py         # /users and /users/me
            └── rag.py           # /rag/query
```

---

## Concepts & Patterns

### Dependency Injection
- Implemented in `src/app/dependencies.py` with FastAPI's `Depends()`.
- Provides decoupled constructors for core components (DB, services, providers).

### Registry
- `src/app/registry.py` defines mappings:
  - **LLM_PROVIDERS**: e.g. OpenAILLMAdapter
  - **EMBEDDING_PROVIDERS**: e.g. OpenAIEmbeddingAdapter
  - **USER_REPOSITORY_PROVIDERS**: e.g. PostgresUserRepository

### Ports & Adapters
- **Ports** (`src/app/ports/`): abstract interfaces:
  - `LLMPort` for chat completions
  - `EmbeddingPort` for vector embeddings
  - `UserRepositoryPort` for user persistence
- **Adapters** (`src/app/adapters/`): concrete implementations:
  - `OpenAILLMAdapter` (uses OpenAI SDK)
  - `OpenAIEmbeddingAdapter` (uses OpenAI SDK)
  - `PostgresUserRepository` (SQLAlchemy + AsyncSession)

### Services
- Business logic lives in `src/app/services/`:
  - `UserService`: handles user creation & lookup
  - `LLMService`: wraps LLM chat interactions
  - `RetrievalService`: embeds queries & fetches relevant docs for RAG

### Routers (Routes)
- FastAPI routers in `src/app/routers/`:
  - **`auth.py`**: `/token` endpoint issues JWTs
  - **`users.py`**: `/users` registration, `/users/me` profile
  - **`rag.py`**: `/rag/query` for Retrieval-Augmented Generation

### Schemas & Models
- **Schemas** (`src/app/schemas.py`): Pydantic models for request/response validation
- **Models** (`src/app/models.py`): SQLAlchemy ORM definitions (e.g. `User` table)

---

## Configuration

- Environment variables are loaded by Pydantic `BaseSettings` in `config.py` via the `.env` file.
- Required vars:
  - `DATABASE_URL`
  - `OPENAI_API_KEY`
  - `SECRET_KEY`
  - `USER_SALT`
  - (Optionally) `LLM_PROVIDER`, `EMBEDDING_PROVIDER`, `USER_REPOSITORY`

Copy `.env` to set your local credentials before running.

---

## Local Development & Docker

1. **Environment**: Duplicate `.env` with real values.
2. **Docker Build**:
   ```bash
   docker build -t rag-api:local -f docker/Dockerfile .
   ```
3. **Run Container**:
   ```bash
   docker run --env-file .env -p 80:80 rag-api:local
   ```
4. **VS Code Dev Container**: Open `base_app` folder in VS Code and reopen in container (uses `.devcontainer`).

---

## Database Migrations with Alembic

1. **Initialize** (already configured): check `alembic.ini` & `alembic/env.py`.
2. **Create Revision**:
   ```bash
   alembic revision --autogenerate -m "<message>"
   ```
3. **Apply Migrations**:
   ```bash
   alembic upgrade head
   ```

Migrations live under `alembic/versions/` and are automatically applied by the Kubernetes Job.

---

## Kubernetes Deployment on Azure AKS (Helm)

### Prerequisites
- Azure CLI, kubectl & Helm installed
- Azure Resource Group, Azure Container Registry (ACR), and AKS cluster with ACR integrated

### 1. Build & Push Image to ACR
```bash
az acr login --name <ACR_NAME>
docker build -t <ACR_NAME>.azurecr.io/rag-api:latest -f docker/Dockerfile .
docker push <ACR_NAME>.azurecr.io/rag-api:latest
```

### 2. Install Cert-Manager & ClusterIssuer
```bash
# Add cert-manager repo & install
helm repo add jetstack https://charts.jetstack.io
helm install cert-manager jetstack/cert-manager   --namespace cert-manager --create-namespace --version v1.11.0

# Create your azure-dns secret in cert-manager namespace
kubectl create secret generic azure-dns   --namespace cert-manager   --from-literal=subscription-id=<SUB_ID>   --from-literal=tenant-id=<TENANT_ID>   --from-literal=client-id=<CLIENT_ID>   --from-literal=client-secret=<CLIENT_SECRET>

# Deploy our ClusterIssuer
helm upgrade --install cert-infra helm/cert-infra   --namespace cert-manager
```

### 3. Deploy RAG API with Helm
1. **Apply Secrets** (fills in DATABASE_URL, API keys, etc):
   ```bash
   kubectl apply -f helm/rag-api/app-secrets.yaml --namespace default
   ```
2. **Install/Upgrade Chart**:
   ```bash
   helm upgrade --install rag-api helm/rag-api      --namespace default --create-namespace
   ```
3. **Run Alembic Migrations** via Kubernetes Job:
   ```bash
   kubectl get jobs -n default
   kubectl logs job/alembic-upgrade -n default
   ```
4. **Verify Service & Ingress**
   ```bash
   kubectl get svc,ing -n default
   ```

---

## Summary

This project demonstrates a production-ready FastAPI service with:

- **Clean Architecture**: DI, Registry, Ports & Adapters, Services, Routers
- **Security**: JWT auth & hashed passwords
- **Async DB Access**: SQLAlchemy + Alembic migrations
- **Containerization**: Docker & VS Code Dev Containers
- **Cloud Deployment**: Helm charts on Azure AKS with cert-manager

Follow these guides to extend features, add tests, and deploy confidently. 🚀
