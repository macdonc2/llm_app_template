"""
manager.py

This module defines custom user management logic for a microservices-based FastAPI application, leveraging the FastAPI Users package and async integrations. It provides business rules and extensibility points for user registration, password validation, reset/verification token handling, and post-registration processes.

Overview:
---------
The `UserManager` class extends `fastapi_users`' base user manager functionality, introducing custom hooks and validation steps to enforce organizational policies. It forms a core part of the authentication and user lifecycle management microservice, interacting with an async SQLAlchemy backend.

Key Features:
-------------
- **Password Policy Enforcement:** Ensures all newly registered users set a password meeting a minimum length requirement, raising clear exceptions for violations.
- **Secure Token Management:** Manages secrets for user password reset and verification workflows, using application-level secure settings.
- **Lifecycle Hooks:** Automatically sets new users as inactive on registration, supporting workflows where admin approval is mandatory before activation. Post-registration logic is handled using the `on_after_register` async hook.
- **FastAPI Dependency Injection:** Exposes `get_user_manager` as a dependency for seamless integration into FastAPI routes or background jobs.
- **Extensible and Modular:** By inheriting from FastAPI Users' manager and UUID mixin, this class enables robust, scalable, and extensible user management for distributed, microservices-oriented systems.

Typical Usage:
--------------
Inject `get_user_manager` as a dependency into FastAPI routes that need custom user registration, authentication, or management workflows. The design enables plugging in business rules at crucial user management checkpoints.

Security Considerations:
------------------------
All sensitive tokens (for resets and verification) and user status changes are managed with well-defined secrets and are extensible for advanced security requirements in production or regulated environments.

Dependencies:
-------------
- FastAPI and fastapi-users
- Async SQLAlchemy database integration
- Project-specific configuration and user schema

"""

import uuid
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin, InvalidPasswordException
from fastapi_users.db import SQLAlchemyUserDatabase

from app.db.user import get_user_db
from app.models import User
from app.schemas import UserCreate
from app.config import settings

SECRET = settings.secret_key
ACCESS_TOKEN_EXPIRE = settings.access_token_expire_minutes * 60

class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET
    """
    Manager class for handling user operations such as password resets and verifications.

    Attributes:
        reset_password_token_secret (str): Secret used for generating password reset tokens.
        verification_token_secret (str): Secret used for generating verification tokens.
    """

    async def validate_password(self, password: str, user: UserCreate) -> None:
        """
        Validate the given password for the user during registration.

        Ensures the password meets minimum length requirements.

        Args:
            password (str): The password to validate.
            user (UserCreate): The user registration data.

        Raises:
            InvalidPasswordException: If the password is shorter than 8 characters.
        """
        
        if len(password) < 8:
            raise InvalidPasswordException(
                reason="Password must be at least 8 characters"
            )
        await super().validate_password(password, user)

    async def on_after_register(
        self, user: User, request: Optional[Request] = None
    ):
        """
        Perform actions after a new user registers.

        Sets the new user to inactive and logs the event.

        Args:
            user (User): The newly registered user.
            request (Optional[Request]): The HTTP request context (optional).
        """
        
        await self.user_db.update(user, {"is_active": False})
        print(f"New user registered: {user.id}")

async def get_user_manager(
    user_db: SQLAlchemyUserDatabase = Depends(get_user_db),
) -> UserManager:
    """
    Yield a UserManager instance for managing user-related operations.

    Args:
        user_db (SQLAlchemyUserDatabase): The user database dependency.

    Yields:
        UserManager: An instance of UserManager configured with the provided user database.
    """

    yield UserManager(user_db)
