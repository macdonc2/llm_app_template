# src/app/db/user.py
from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.core import get_async_session
from app.models import User

async def get_user_db(
    session: AsyncSession = Depends(get_async_session),
):
    """
    Yield a SQLAlchemyUserDatabase instance for user operations.

    Args:
        session (AsyncSession): The asynchronous database session dependency.

    Yields:
        SQLAlchemyUserDatabase: User database instance configured with the provided session and User model.
    """
    
    # session first, model second
    yield SQLAlchemyUserDatabase(session, User)
