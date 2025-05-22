"""
user.py

This module provides a dependency-injection mechanism for accessing the user database in a FastAPI, microservices-oriented application architecture. It leverages asynchronous SQLAlchemy sessions and integrates seamlessly with the `fastapi-users` authentication ecosystem, ensuring scalability and modularity.

Overview:
---------
Defines the `get_user_db` async dependency that yields an instance of `SQLAlchemyUserDatabase` configured for your custom `User` ORM model. This allows application routes and service layers to perform database operations (CRUD, authentication, etc.) against user records using an async interface, as required in modern, microservices-based FastAPI projects.

Key Features:
-------------
- **Async SQLAlchemy Integration:** Ensures non-blocking database operations with `AsyncSession`, critical for high-concurrency in microservices deployments.
- **FastAPI Dependency Injection:** Designed as a dependency (`Depends`) to be consumed by API routes and background services, ensuring clean separation and reusability.
- **Compliance with FastAPI-Users:** Integrates with the `fastapi-users` plugin, supporting advanced authentication, registration, and user management with minimal boilerplate.
- **UUID-based Primary Keys:** Explicitly configures user IDs as UUIDs, aiding in distributed system uniqueness and interoperability.

Intended Usage:
---------------
Meant to be used as a FastAPI dependency injection target, enabling handlers to easily access user storage functionality. Fosters stateless, composable services, a hallmark of effective microservices architectures.

Dependencies:
-------------
- SQLAlchemy Async ORM
- FastAPI
- fastapi-users
- Project-specific User model and async session getter

"""

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
