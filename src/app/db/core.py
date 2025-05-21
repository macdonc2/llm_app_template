from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config import settings

DATABASE_URL = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_db() -> AsyncSession:
    """
    Provide a database session using an asynchronous context manager.

    Yields:
        AsyncSession: An active SQLAlchemy asynchronous session.
    """

    async with AsyncSessionLocal() as session:
        yield session

async def get_async_session() -> AsyncSession:
    """
    Provide an asynchronous SQLAlchemy session for database operations.

    Yields:
        AsyncSession: An active asynchronous database session.
    """
    
    async with AsyncSessionLocal() as session:
        yield session
