from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users.db import SQLAlchemyUserDatabase
from app.models import User
from app.db.core import get_async_session

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """
    Yield a SQLAlchemyUserDatabase instance for user data access with async support.

    Args:
        session (AsyncSession): The asynchronous SQLAlchemy session dependency.

    Yields:
        SQLAlchemyUserDatabase: An async user database instance configured for the User model.
    """
    
    yield SQLAlchemyUserDatabase(User, session, id_model=UUID)
