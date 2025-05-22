"""
main.py

This module serves as the main entrypoint for a microservices-based FastAPI application, 
coordinating API routing, security, and middleware configuration for scalable, distributed deployments. 
It exposes authentication, admin, retrieval-augmented generation (RAG), search, and agent inference endpoints, 
while ensuring robust, fine-grained access control using dependency-injected FastAPI-Users guards.

Overview:
---------
- Initializes the FastAPI app instance, setting application-level metadata.
- Configures CORS to enable cross-origin access—suitable for SPA frontends or federated microservice consumption.
- Registers routers for:
  * Authentication (JWT, registration, password reset, etc.)
  * Admin-only user management and audit endpoints
  * User self-management endpoints (guarded for superusers)
  * Retrieval-augmented generation (RAG) pipelines
  * Tavily-powered contextual search
  * Agent-based AI completion/inference
- Applies layered security and role-based access at the router level using FastAPI-Users' session guards for active, verified, and superuser users.

Key Features:
-------------
- **Modular Router Integration:** All domain logic is encapsulated in sub-routers, supporting microservice scalability and separation of concerns.
- **Fine-grained Dependency Injection:** Critical endpoints are protected by user role/verification checks, minimizing risk of privilege escalation or unauthorized access.
- **Plug-and-Play CORS:** Enables easy adaption to API gateway or frontend deployments with flexible CORS headers.
- **Health Endpoint:** Provides a root `GET /` endpoint for basic liveness checks and orchestration tooling.

Intended Usage:
---------------
- Deployed as a central REST API in a microservices environment, either standalone or behind an API gateway or reverse proxy.
- All major domains (authentication, admin, retrieval, summarization, agents) can be independently scaled or refactored as needs grow.

Dependencies:
-------------
- FastAPI, fastapi-users, CORSMiddleware
- Modular routers for authentication, admin, RAG, search, and agent endpoints

Security & Best Practices:
--------------------------
- Explicit user role verification for all sensitive routers; superuser-only routes for admin actions.
- Promotes defense-in-depth and minimizes exposure of high-powered features (e.g., AI agents, summarization).

"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.auth.admin import router as admin_router
from app.auth.router import router as auth_router, fastapi_users
from app.schemas import UserRead, UserUpdate
from app.routers.rag import router as rag_router
from app.routers.agent import router as agent_router
from app.routers.tavily import router as tavily_router

# Dependencies to protect endpoints
current_active = fastapi_users.current_user(active=True)
current_verified = fastapi_users.current_user(active=True, verified=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)

app = FastAPI(title="Your App with Auth + RAG")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication and admin routes
app.include_router(auth_router)
app.include_router(admin_router)

# User management routes (only superusers)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(current_superuser)],
)

# Public RAG endpoints
app.include_router(rag_router)

# Protected Tavily endpoints (requires active user)
app.include_router(
    tavily_router,
    dependencies=[Depends(current_verified)],
)

# Protected Agent endpoints (requires active + verified user)
app.include_router(
    agent_router,
    dependencies=[Depends(current_verified)],
)

@app.get("/")
async def health_check():
    return {"status": "ok"}