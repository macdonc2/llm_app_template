"""
router.py

This module defines the authentication and user management API endpoints for a microservices-based FastAPI application, utilizing the FastAPI Users framework. It centralizes all authentication logic—including JWT bearer token operations, user registration, password resets, and user profile management—under a single, cohesive router setup.

Overview:
---------
Leverages FastAPI Users' highly-configurable authentication backends to provide secure, scalable user authentication using JWT tokens for stateless sessions. Exposes registration, password reset, and user CRUD interfaces as modular FastAPI routers, adhering to the separation of concerns crucial for microservices design.

Key Features:
-------------
- **JWT Authentication:** Implements a robust JWT bearer authentication system with configurable token lifetimes and secure secret management, enabling stateless session handling suitable for distributed microservices.
- **Extensible User Management:** Provides registration, login, password reset, and user update endpoints, all aligning with project schemas and leveraging dependency injection for custom logic.
- **Central Router Composition:** Aggregates all authentication and user management endpoints under a single APIRouter instance, simplifying inclusion into the application's API gateway or service orchestrator.
- **Type-Safe and Modern:** Utilizes type-safe generics and Pydantic schemas, ensuring integration consistency across microservices and facilitating API documentation.
- **Convenient Dependency Injection:** Relies on application settings and user manager dependency injection for flexible configuration, security, and testability.

Usage/Integration:
------------------
Typically included as a sub-router in the main FastAPI application or related microservice. Endpoints are grouped by prefix and tag for clean OpenAPI docs and easy route management. Designed to be stateless and horizontally scalable, ideal for cloud-native and containerized deployments.

Security Considerations:
------------------------
All authentication operations utilize JWTs signed with a securely managed secret, and sensitive endpoints (like password reset) are protected per best practices. Configuration values are sourced from environment-aware settings, promoting compliance in production environments.

Dependencies:
-------------
- FastAPI and fastapi-users
- Project-specific user manager and schemas
- Application-wide settings (secrets, token TTL)

"""

import uuid
from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)

from app.auth.manager import get_user_manager
from app.schemas import UserRead, UserCreate, UserUpdate
from app.config import settings

router = APIRouter()

# Transport + strategy factory
bearer_transport = BearerTransport(tokenUrl="/auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    """
    Create and return a JWTStrategy instance configured with application settings.

    Returns:
        JWTStrategy: An instance of JWTStrategy using the application's secret key
        and token lifetime.
    """
    
    return JWTStrategy(
        secret=settings.secret_key,
        lifetime_seconds=settings.access_token_expire_minutes * 60,
    )

# Build the JWT backend
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

# Create your FastAPIUsers instance (only manager + backends)
fastapi_users = FastAPIUsers[UserRead, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

# Wire up all the routers
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
