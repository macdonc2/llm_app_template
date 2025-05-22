"""
auth.py

This module configures authentication and user management endpoints for a microservices-based FastAPI application,
leveraging the fastapi-users library to provide secure, extensible user workflows and JWT-based authentication. It sets up the required authentication backend, session strategies, and exposes modular routes for registration, login, verification, password reset, and user CRUD operations.

Overview:
---------
- Implements secure JWT authentication using a configurable secret key and token lifetime, with tokens transported via Bearer headers.
- Orchestrates fastapi-users’ high-level abstractions for user registration, authentication, email verification, password resets, and user profile management. 
- Uses reusable and dependency-injectable user database access, easily swappable to target different databases or mock stores.

Key Features:
-------------
- **JWT Authentication:** Configures and exposes JWT bearer authentication, providing stateless security for distributed microservices.
- **Modular User Workflows:** Includes routers for registration (`/auth/register`), login (`/auth/jwt/login`), password reset, email verification, and user CRUD, all under relevant prefixes with appropriate Pydantic schema serialization/deserialization.
- **Separation of Concerns:** Cleanly separates authentication, user logic, and database persistence, supporting hexagonal architecture and high scalability.
- **Dependency Injection:** Utilizes dependency injection for user store access, allowing for straightforward testing and backend replacement.
- **Strong Typing and Schema Validation:** Integrates project schemas for full type- and data-validation on all endpoints.

Intended Usage:
---------------
- Plugged directly into the main FastAPI application as a sub-router, providing a drop-in solution for core authentication flows in a microservice or API gateway.
- Meant to be reused across multiple services with shared authentication concerns or extended to support custom security policies.

Dependencies:
-------------
- FastAPI and fastapi-users
- SQLAlchemy (via async user DB)
- Application-specific models (`User`), schemas (`UserCreate`, `UserRead`, `UserUpdate`), and settings/configuration

Security Considerations:
------------------------
- All token operations are guarded with a robust, application-configured secret.
- Token and sensitive values never returned in cleartext.
- User workflows (registration, verification, reset) gated with modern secure patterns.

"""

import uuid
from fastapi import APIRouter
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy

from app.db.user import get_user_db
from app.models import User
from app.schemas import UserCreate, UserRead, UserUpdate
from app.config import settings

router = APIRouter()

# How the token is transported
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

# JWT strategy
def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.SECRET_KEY, lifetime_seconds=3600)

# Authentication backend
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

# FastAPI-Users instance
fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_db,
    [auth_backend],
    User,
    UserCreate,
    UserRead,
    UserUpdate,
)

# Mount the built-in FastAPI-Users routers
router.include_router(
    fastapi_users.get_register_router(UserCreate, UserRead),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
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
