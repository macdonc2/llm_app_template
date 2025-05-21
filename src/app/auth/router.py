# src/app/auth/router.py
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
