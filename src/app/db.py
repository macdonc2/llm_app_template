from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .config import settings

DATABASE_URL = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_db() -> AsyncSession:
    """
    Provide a database session for dependency injection.

    This asynchronous generator yields an instance of `AsyncSession` 
    from the sessionmaker `AsyncSessionLocal`, ensuring the session 
    is properly opened and closed within a context manager.

    Yields:
        AsyncSession: An active SQLAlchemy async database session.
    """

    async with AsyncSessionLocal() as session:
        yield session

async def get_async_session() -> AsyncSession:
    """
    Dependency provider that yields an asynchronous SQLAlchemy session.

    This function is intended for use with dependency injection in frameworks
    like FastAPI. It creates an instance of `AsyncSession` from the configured 
    sessionmaker `AsyncSessionLocal` and ensures that the session is properly 
    closed after use.

    Yields:
        AsyncSession: A SQLAlchemy asynchronous session instance.
    """
    
    async with AsyncSessionLocal() as session:
        yield session
