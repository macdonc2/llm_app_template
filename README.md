# RAG + Auth API Starter

A FastAPI-based “RAG + Auth” service scaffolded with:

- **Ports & Adapters** (Hexagonal) architecture  
- **Pydantic BaseSettings** for configuration  
- **Jinja2** templates for prompts  
- **Async SQLAlchemy** + Postgres (with pgvector)  
- **JWT authentication**, user management via per-user salted HMAC IDs  
- **Docker** & **Helm** deployment to AKS (NGINX Ingress)

---

## Table of Contents

1. [Prerequisites](#prerequisites)  
2. [Project Structure](#project-structure)  
3. [Configuration](#configuration)  
4. [Local Setup & Development](#local-setup--development)  
5. [Docker Image & Registry](#docker-image--registry)  
6. [AKS Deployment with Helm](#aks-deployment-with-helm)  
7. [Database Migrations](#database-migrations)  
8. [Usage & Endpoints](#usage--endpoints)  
9. [Prompts](#prompts)  
10. [Extending Adapters](#extending-adapters)  
11. [Testing](#testing)  
12. [Further Improvements](#further-improvements)

---

## Prerequisites

- **Python 3.11+**  
- **pip**  
- **Docker & Docker Hub** (or Azure Container Registry)  
- **Helm 3**  
- **kubectl**  
- **Azure CLI** (logged in, with `az aks get-credentials`)  
- **Postgres** (we use the Bitnami Helm chart with pgvector)  

---

## Project Structure

```
.
├── helm/
│   └── rag-api/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
│           ├── deployment.yaml
│           ├── service.yaml
│           └── ingress.yaml
├── src/
│   └── app/
│       ├── adapters/
│       │   ├── openai_llm_adapter.py
│       │   ├── openai_embedding_adapter.py
│       │   └── postgres_user_repository.py
│       ├── ports/
│       │   ├── llm_port.py
│       │   ├── embedding_port.py
│       │   └── user_repository_port.py
│       ├── prompts/
│       │   └── rag_query.j2
│       ├── config.py
│       ├── dependencies.py
│       ├── db.py
│       ├── utils.py
│       ├── models.py
│       ├── schemas.py
│       ├── security.py
│       ├── registry.py
│       ├── routers/
│       │   ├── auth.py
│       │   ├── users.py
│       │   └── rag.py
│       └── services/
│           ├── llm_service.py
│           ├── retrieval_service.py
│           └── user_service.py
```

---

## Configuration

All configuration is managed via **environment variables** and Pydantic’s `BaseSettings` in `src/app/config.py`.

Create a `.env` file at the project root:

```ini
DATABASE_URL=postgresql://postgres:secretpassword@my-postgresql.data.svc.cluster.local:5432/postgres
OPENAI_API_KEY=your_openai_api_key
SECRET_KEY=your_jwt_secret_key
USER_SALT=your_global_pepper_string

# Adapter selection (defaults shown)
LLM_PROVIDER=openai
EMBEDDING_PROVIDER=openai
USER_REPOSITORY=postgres

# Jinja2 prompt templates folder (optional override)
PROMPT_PATH=src/app/prompts
```

- **DATABASE_URL**: your Postgres URI  
- **OPENAI_API_KEY**: for LLM & embeddings  
- **SECRET_KEY**: JWT signing secret  
- **USER_SALT**: global “pepper” for per-user ID HMAC  
- **LLM_PROVIDER**, **EMBEDDING_PROVIDER**, **USER_REPOSITORY**: select adapters  
- **PROMPT_PATH**: where Jinja2 finds `.j2` templates  

---

## Local Setup & Development

1. **Create & activate virtual environment**  
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up Postgres locally** (e.g., Docker Compose or local install) and point `DATABASE_URL` to it.  
4. **Run migrations** (see [Database Migrations](#database-migrations)).  
5. **Start FastAPI**  
   ```bash
   uvicorn src.app.main:app --reload --host 0.0.0.0 --port 8000
   ```
6. **Visit docs** at [http://localhost:8000/docs](http://localhost:8000/docs).  

---

## Docker Image & Registry

1. **Build**  
   ```bash
   docker build -t myregistry.azurecr.io/rag-api:latest .
   ```
2. **Push**  
   ```bash
   docker push myregistry.azurecr.io/rag-api:latest
   ```

---

## AKS Deployment with Helm

1. **Add repos**  
   ```bash
   helm repo add bitnami https://charts.bitnami.com/bitnami
   helm repo update
   ```
2. **Install Postgres with pgvector**  
   ```bash
   helm install my-postgresql bitnami/postgresql      --namespace data --create-namespace      --set auth.postgresPassword=secretpassword      --set primary.persistence.size=10Gi
   # Enable pgvector:
   kubectl exec -n data statefulset/my-postgresql --      psql -U postgres -c "CREATE EXTENSION IF NOT EXISTS vector;"
   ```
3. **Deploy your API**  
   ```bash
   helm upgrade --install rag-api helm/rag-api      --set image.repository=myregistry.azurecr.io/rag-api      --set image.tag=latest
   ```
4. **Configure DNS** to point `api.example.com` (or your host) at the AKS Ingress IP.  

---

## Database Migrations

This project uses **Alembic** (optional, but recommended):

1. **Initialize** (if not done):  
   ```bash
   alembic init alembic
   ```
2. **Configure** `alembic/env.py` to import:
   ```python
   from src.app.db import engine
   from src.app.models import Base
   target_metadata = Base.metadata
   ```
3. **Generate & apply**  
   ```bash
   alembic revision --autogenerate -m "create users table"
   alembic upgrade head
   ```
4. **Add salt column** when prompted:
   ```bash
   alembic revision --autogenerate -m "add salt column to users"
   alembic upgrade head
   ```

---

## Usage & Endpoints

### Authentication

- **Register**  
  ```
  POST /users
  Content-Type: application/json

  {
    "email": "alice@example.com",
    "password": "secret"
  }
  ```
  → Returns `UserRead` with `id`, `email`, `created_at`.

- **Login**  
  ```
  POST /token
  Content-Type: application/x-www-form-urlencoded

  username=alice@example.com&password=secret
  ```
  → Returns `{ "access_token": "...", "token_type": "bearer" }`.

- **Get Profile**  
  ```
  GET /users/me
  Authorization: Bearer <ACCESS_TOKEN>
  ```
  → Returns current user.

- **Update Profile**  
  ```
  PATCH /users/me
  Authorization: Bearer <ACCESS_TOKEN>
  Content-Type: application/json

  {
    "email": "new@example.com",
    "password": "newpass"
  }
  ```

### RAG Query

```
POST /rag/query
Authorization: Bearer <ACCESS_TOKEN>
Content-Type: application/json

{
  "query": "What is RAG?"
}
```
→ Returns `{ "answer": "..." }`.

---

## Prompts

All prompts live as **Jinja2** templates in `src/app/prompts/`.  
Example **`rag_query.j2`**:

```jinja
You are a helpful assistant. Use the following context documents:
{% for doc in docs %}
{{ doc }}
{% endfor %}

Answer the question: {{ query }}
```

---

## Extending Adapters

1. **Add Port** in `src/app/ports/` (e.g., `my_llm_port.py`).  
2. **Implement Adapter** in `src/app/adapters/` (e.g., `my_llm_adapter.py`).  
3. **Register** in `src/app/registry.py` under the appropriate dict.  
4. **Set** the matching name in your `.env` (e.g., `LLM_PROVIDER=my_custom_llm`).  

---

## Testing

- Write unit tests against your **ports** by mocking adapters.  
- Use Testcontainers or a local Postgres for integration tests.  
- Example Pytest fixture for FastAPI:

  ```python
  from fastapi.testclient import TestClient
  from src.app.main import app

  client = TestClient(app)

  def test_health():
      r = client.get("/health")
      assert r.status_code == 200
  ```

---

