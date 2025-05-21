# LLM App Template

A comprehensive, beginner-to-expert guide for understanding, running, deploying, and extending the LLM App Template. This template demonstrates best practices in API design, tool orchestration via MCP servers, database migrations, containerization, and cloud-native deployment with Helm on Azure AKS. This guide includes detailed explanations, real-world analogies, code examples, dependency lists, and troubleshooting tips.

---

## Table of Contents

1. [Overview](#overview)  
2. [Architecture & Programming Patterns](#architecture--programming-patterns)  
   - Dependency Injection (DI)  
   - Service Registry  
   - Ports & Adapters  
3. [Setup & Dependencies](#setup--dependencies)  
4. [Database Migrations with Alembic](#database-migrations-with-alembic)  
5. [Docker Compose & Local Development](#docker-compose--local-development)  
6. [Specialized Routes & MCP Integration](#specialized-routes--mcp-integration)  
7. [Helm Charts & AKS Deployment](#helm-charts--aks-deployment)  
8. [Extending the Application](#extending-the-application)  
9. [Troubleshooting Tips & Tricks](#troubleshooting-tips--tricks)  
10. [Contributing](#contributing)  

---

## Overview

Welcome, developer! This template bundles a full-stack microservice architecture:

- **FastAPI** for RESTful HTTP endpoints  
- **gRPC/SSE-based Agent** for orchestrating tool calls (MCP servers)  
- **SQLAlchemy & Alembic** for ORM and database version control  
- **Docker Compose** for local multi-container setups  
- **Helm & Azure AKS** for production-grade Kubernetes deployments  

We start with core concepts, reinforce with analogies, dive into setup, then deploy to Azure. By the end, you'll understand the “why” behind each pattern and the “how” to extend and troubleshoot effectively.

---

## Architecture & Programming Patterns

### 1. Dependency Injection (DI)

**Concept:** Injecting a component’s dependencies at runtime rather than hardcoding them.

**Analogy:**  
Imagine a power strip with multiple outlets. Instead of building different chargers directly into your power supply, you plug in any device’s charger as needed. The power strip doesn’t care what you plug in—it just provides electricity.

**Why DI?**  
- **Loose Coupling:** Services don’t instantiate their dependencies; they receive them externally.  
- **Testability:** Swap real services with mocks or fakes easily.  
- **Flexibility:** Change implementations without altering business logic.

**Example:**
```python
# Define a user repository interface (abstract)
class UserRepository:
    def get_user(self, user_id: str) -> User:
        raise NotImplementedError

# Concrete implementation using SQLAlchemy
class SqlUserRepository(UserRepository):
    def __init__(self, session):
        self.session = session

    def get_user(self, user_id: str) -> User:
        return self.session.query(UserModel).get(user_id)

# Service that depends on the repository
class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def fetch_user_profile(self, user_id: str) -> UserProfile:
        user = self.user_repo.get_user(user_id)
        return UserProfile.from_model(user)

# At application startup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db_session = SessionLocal()

# Injecting the SQL repository into the service
user_service = UserService(user_repo=SqlUserRepository(db_session))
```

**Usage Guidance:**  
- Define interfaces or abstract base classes for dependencies.  
- Instantiate and wire dependencies in a single *composition root* (e.g., FastAPI startup event).  
- Avoid `import`ing concrete implementations within business logic.

---

### 2. Service Registry

**Concept:** A centralized lookup for services used across the application.

**Analogy:**  
Think of a hotel concierge desk. Guests ask the concierge for services (taxis, tours, room service). The desk maintains a directory and forwards your request to the appropriate vendor.

**Why Registry?**  
- **Global Access Point:** Retrieve services anywhere without deep import chains.  
- **Late Binding:** Register services after instantiation, enabling dynamic plugins.  
- **Circular Import Avoidance:** No need to import modules in each other.

**Example:**
```python
class ServiceRegistry:
    _services: dict[str, object] = {}

    @classmethod
    def register(cls, name: str, service: object) -> None:
        cls._services[name] = service

    @classmethod
    def get(cls, name: str) -> object:
        if name not in cls._services:
            raise KeyError(f"Service '{name}' not found.")
        return cls._services[name]

# Registering services at startup
ServiceRegistry.register("user_service", user_service)
ServiceRegistry.register("search_service", SearchService())

# Retrieving elsewhere
search_svc = ServiceRegistry.get("search_service")
results = search_svc.search("query terms")
```

**Usage Guidance:**  
- Register exactly once, ideally in the main application entrypoint.  
- Clear or override registrations in tests to control dependencies.  
- Use descriptive keys to avoid confusion.

---

### 3. Ports & Adapters (Hexagonal Architecture)

**Concept:** Define *ports* (interfaces) for your core domain logic and *adapters* (implementations) for external systems.

**Analogy:**  
Electrical outlets (ports) follow standard shapes. You may have different plugs (adapters) for various countries, but the outlet interface stays the same.

**Why Ports & Adapters?**  
- **Decoupling:** Core domain code knows nothing about external details.  
- **Swappability:** Replace or mock external systems without touching business logic.  
- **Testability:** Adapters are easily faked in unit tests.

**Example:**
```python
# Domain port (interface)
class NotificationPort(ABC):
    @abstractmethod
    def send(self, recipient: str, message: str) -> None:
        pass

# SMTP adapter
class SmtpNotificationAdapter(NotificationPort):
    def __init__(self, smtp_client):
        self.smtp = smtp_client

    def send(self, recipient: str, message: str) -> None:
        self.smtp.send_email(to=recipient, body=message)

# SMS adapter
class SmsNotificationAdapter(NotificationPort):
    def __init__(self, sms_client):
        self.sms = sms_client

    def send(self, recipient: str, message: str) -> None:
        self.sms.send_text(to=recipient, text=message)

# Business logic uses only the port
def notify_user(port: NotificationPort, user_email: str, text: str):
    port.send(user_email, text)

# Wiring at startup
smtp_adapter = SmtpNotificationAdapter(smtp_client)
ServiceRegistry.register("notifier", smtp_adapter)
```

**Usage Guidance:**  
- Keep port interfaces minimal and focused on domain needs.  
- Place ports in a `ports/` or `domain/ports/` folder.  
- Adapters live under `adapters/` with clear naming (e.g., `adapters/smtp.py`).

---

## Setup & Dependencies

**Required Versions & Tools:**
- **Python:** 3.11 or higher  
- **PostgreSQL:** 15.x  
- **Docker & Docker Compose:** v20+  
- **Helm:** 3.x  
- **Azure CLI:** 2.0+ with `aks-preview` extension  
- **kubectl:** v1.25+

**Repository Structure:**
```
.
├── alembic/                  # Alembic migration environment
├── app/                      # FastAPI application code
│   ├── main.py
│   ├── routes/
│   ├── services/
│   └── models.py
├── agent/                    # gRPC/SSE agent service
├── adapters/                 # Ports & Adapters implementations
├── ports/                    # Domain port interfaces
├── charts/                   # Helm chart templates
├── docker-compose.yaml
├── Dockerfile
├── requirements.txt
└── README.md
```

**Environment Variables:**
- `DATABASE_URL` – PostgreSQL connection string  
- `ALEMBIC_CONFIG` – Path to `alembic.ini`  
- `AGENT_HOST`, `AGENT_PORT` – Agent service settings

Install Python deps:
```bash
pip install -r requirements.txt
```

---

## Database Migrations with Alembic

Alembic tracks database schema versions:

1. **Initialize**: `alembic init alembic`  
   Creates `alembic.ini` and `alembic/` folder.

2. **Configure**: In `alembic/env.py`, set `target_metadata = Base.metadata` to point to SQLAlchemy models.

3. **Generate**:  
   ```bash
   alembic revision --autogenerate -m "Add orders table"
   ```  
   Compares models to DB; creates migration script.

4. **Apply**:  
   ```bash
   alembic upgrade head
   ```

5. **Downgrade (if needed)**:  
   ```bash
   alembic downgrade -1
   ```

**Dependencies:**
- `alembic>=1.9.0`  
- `sqlalchemy>=1.4.0`  
- `psycopg2-binary`

**Common Issues & Fixes:**
- **Missing Metadata**: Migrations empty? Ensure `import models` in `env.py`.  
- **Circular Imports**: Use late imports inside functions or dedicated metadata module.  
- **Multiple Heads**: Conflicting migrations?  
  ```bash
  alembic history --verbose
  alembic merge <rev1> <rev2> -m "Merge heads"
  ```  
- **Version Table Not Found**: Manually create `alembic_version` table or run `stamp head`.

---

## Docker Compose & Local Development

Use Compose for spinning up dependencies:

```yaml
version: "3.8"
services:
  db:
    image: postgres:15
    restart: always
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: appdb
    volumes:
      - db_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  api:
    build: .
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - .:/usr/src/app
    environment:
      DATABASE_URL: postgresql://postgres:secret@db:5432/appdb
    depends_on:
      - db
    ports:
      - "8000:8000"

  agent:
    build: ./agent
    command: uvicorn agent.main:app --host 0.0.0.0 --port 8001 --reload
    volumes:
      - ./agent:/usr/src/agent
    environment:
      AGENT_TOOL_URL: http://api:8000
    depends_on:
      - api
    ports:
      - "8001:8001"

volumes:
  db_data:
```

**Usage Guidance:**  
- Use `--reload` in development to auto-reload on code changes.  
- Persist data with named volumes (`db_data`).  
- Link services via Compose network; use service names (`db`, `api`) in connection strings.

---

## Specialized Routes & MCP Integration

This application defines both domain-specific routes and a generic agent proxy:

### Tavily Search Route

Route: `POST /tavily/search`

**Flow:**  
1. Receive search query payload  
2. Retrieve `search_service` from registry  
3. Call `search(q)` and return results  

```python
@app.post("/tavily/search")
def tavily_search(q: str):
    search_service: SearchService = ServiceRegistry.get("search_service")
    results = search_service.search(q)
    return {"results": results}
```

**Usage Guidance:**  
- Validate input using Pydantic models.  
- Handle exceptions to return meaningful HTTP statuses.

### General Agent Route

Route: `POST /agent`

**Flow:**  
1. Accept `ToolRequest` containing tool name and parameters  
2. Lookup MCP client (e.g., `CalculatorMCPClient`)  
3. Forward request over gRPC or SSE  
4. Stream or return the response  

```python
@app.post("/agent")
async def agent_proxy(request: ToolRequest):
    tool_client = ServiceRegistry.get(f"{request.tool_name}_client")
    response = await tool_client.call(request.payload)
    return response
```

**Usage Guidance:**  
- Support both synchronous and streaming responses.  
- Log request/response for audit and debugging.

---

## Helm Charts & AKS Deployment

### Chart Structure

```
charts/
├── Chart.yaml         # Chart metadata
├── values.yaml        # Default configuration
└── templates/
    ├── deployment.yaml
    ├── service.yaml
    ├── ingress.yaml
    └── _helpers.tpl
```

### values.yaml Highlights

```yaml
replicaCount: 2

image:
  repository: myregistry/llm-app
  pullPolicy: IfNotPresent
  tag: "v1.0.0"

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: true
  hosts:
    - host: llm-app.example.com
      paths: ["/"]

resources: {}
nodeSelector: {}
tolerations: []
affinity: {}
```

### Deploy Steps

1. **Login & Create AKS Cluster**  
   ```bash
   az login
   az group create -n myRg -l eastus
   az aks create -g myRg -n myAks --node-count 2 --enable-addons monitoring --generate-ssh-keys
   az aks get-credentials -g myRg -n myAks
   ```

2. **Add Helm Repo & Install**  
   ```bash
   helm dependency update charts/llm-app
   helm install llm-app charts/llm-app -f charts/llm-app/values.yaml
   ```

3. **Upgrade on Changes**  
   ```bash
   helm upgrade llm-app charts/llm-app -f charts/llm-app/values.yaml
   ```

**Troubleshooting Tips:**  
- **ImagePullBackOff:** Configure `imagePullSecrets` in `values.yaml`.  
- **Pending Pods:** Check `kubectl describe pod <pod>` for scheduling issues.  
- **Ingress 404:** Verify Ingress Controller is installed (`az aks enable-addons ingress-appgw`) and DNS record points to controller IP.  
- **Helm Dry Run:**  
  ```bash
  helm upgrade --install --dry-run charts/llm-app
  ```

---

## Extending the Application

### Adding a New MCP Server

1. **Create Service**  
   - Build a Python project in `services/<tool_name>`.  
   - Define gRPC proto and implement server with FastMCP.  
2. **Containerize & Compose**  
   - Write `Dockerfile`, update `docker-compose.yaml`.  
3. **Register Client**  
   ```python
   from services.<tool_name>.client import ToolNameClient
   ServiceRegistry.register("<tool_name>_client", ToolNameClient(host, port))
   ```
4. **Expose Route (Optional)**  
   ```python
   @app.post(f"/tools/{tool_name}")
   async def call_tool(request: ToolRequest):
       client = ServiceRegistry.get("<tool_name>_client")
       return await client.call(request.params)
   ```

### Adding a Specialized Route

1. **Define Pydantic Schema** in `app/schemas/`.  
2. **Implement Service Logic** injecting dependencies via DI.  
3. **Register Service** in startup.  
4. **Add FastAPI Route** mapping input -> service -> output.

---

## Troubleshooting Tips & Tricks

- **Alembic “No changes detected”:**  
  - Confirm `target_metadata` includes all models.  
  - Run `alembic revision --autogenerate -m "desc"` after `import models`.
- **Docker “bind: address already in use”:**  
  - Change host ports or stop conflicting services.  
- **Helm “render error”:**  
  - Use `helm lint charts/llm-app`.  
- **K8s “CrashLoopBackOff”:**  
  - Inspect logs: `kubectl logs <pod>`.  
  - Describe Pod for events: `kubectl describe pod <pod>`.

---

## Contributing

We welcome all contributions!

1. Fork the repo.  
2. Create a feature branch (`feature/your-feature`).  
3. Write tests and update documentation.  
4. Submit a Pull Request and reference any related issues.  
5. Ensure CI checks pass before merging.

---

Thank you for using the LLM App Template! We hope this guide empowers you to build, deploy, and scale robust microservices with confidence.
