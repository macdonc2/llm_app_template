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
