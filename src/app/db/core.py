"""
core.py

This module configures and exposes asynchronous SQLAlchemy database session management
for a microservices-based FastAPI application. It abstracts the creation and lifecycle
of PostgreSQL-backed async database sessions and provides dependency-injection–ready
helpers, enabling scalable, non-blocking data access throughout the service.

Overview:
---------
- Initializes the SQLAlchemy async engine with connection parameters sourced
  from application settings, converting a standard PostgreSQL DSN to asyncpg format.
- Provides async sessionmaker factory (`AsyncSessionLocal`) for efficient session creation,
  crucial for high-concurrency microservices.
- Exposes `get_db` and `get_async_session` dependency providers, yielding AsyncSession
  objects for use in FastAPI endpoints, background tasks, and service layers.

Key Features:
-------------
- **Async Database Access:** Enables non-blocking DB operations, a necessity in high-throughput,
  distributed FastAPI microservices.
- **Central Session Management:** Ensures reliable, repeatable session lifecycle handling
  using context managers (session close/cleanup on exit).
- **Configuration-Driven:** Reads connection parameters from application-level config,
  promoting portability across environments and deployments.
- **Dependency Injection Ready:** Designed for seamless integration into FastAPI's
  dependency injection system—any route, service, or worker can simply `Depends(get_async_session)`.

Usage Pattern:
--------------
- Inject `get_async_session` or `get_db` directly into FastAPI route handlers,
  services, or repositories for reliable, managed session scope.
- Recommended as the sole session entry point in microservices for consistency and
  to prevent connection leaks.

Dependencies:
-------------
- SQLAlchemy (asyncpg dialect)
- FastAPI
- Application/project config for `database_url`

Security/Scalability Notes:
---------------------------
Async engine and session handling ensure the service is suitable for
stateless, horizontally scalable deployments that are central to
microservices-based designs.

"""

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
