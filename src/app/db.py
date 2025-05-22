"""
db.py

This module configures and provides asynchronous SQLAlchemy database session management
for a microservices-based FastAPI application. It serves as the central factory and dependency
provider for acquiring and releasing database sessions in a non-blocking, scalable manner, making it ideal
for high-concurrency microservices deployments.

Overview:
---------
- Initializes the SQLAlchemy async engine and sessionmaker using database credentials from environment-driven settings.
- Supports PostgreSQL with asyncpg, adapting synchronous DSNs transparently for async compatibility.
- Provides standardized async dependency providers (`get_db` and `get_async_session`) for FastAPI, ensuring all
  database-consuming routes, tasks, and service layers share consistent, managed resource lifecycles.

Key Features:
-------------
- **Async, Non-blocking I/O:** Enables safe, concurrent database access that does not block the event loop, a critical
  requirement for high-performance FastAPI microservices.
- **Context-managed Sessions:** Uses async context managers to guarantee all sessions are properly closed after use, 
  preventing memory leaks and connection pool exhaustion.
- **Centralized Configuration:** Pulls database URL and key parameters from a strongly-typed settings object, promoting
  repeatability, twelve-factor app principles, and environment-agnostic deployment.
- **Dependency Injection Ready:** Designed for seamless use with FastAPI's dependency injection system, making database
  sessions available application-wide with a single import.

Usage:
------
- Import and inject `get_db` or `get_async_session` into API routes, repositories, service layers, or background jobs
  for all read/write access to the database in your microservice.
- Use as the foundation for implementing repositories or pattern-based database access strategies.

Dependencies:
-------------
- SQLAlchemy async ORM (with "asyncpg" driver for PostgreSQL)
- FastAPI (for dependency injection)
- Pydantic-configured application settings module

Security & Scalability:
-----------------------
- Ensures database credentials and configuration are never hard-coded—always pulled from externalized settings.
- Designed for horizontal scaling: sessions are short-lived, stateless, and isolated per request or task.

"""

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
