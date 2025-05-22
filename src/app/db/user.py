"""
user.py

This module provides a dependency-injectable interface for user database operations within
a microservices-based FastAPI application architecture. It abstracts creation of the
asynchronous, SQLAlchemy-backed user store, making it readily available to authentication,
registration, and user profile features through FastAPI’s dependency system.

Overview:
---------
- Defines the `get_user_db` function as a FastAPI dependency, yielding a `SQLAlchemyUserDatabase`
  instance. This integrates with the fastapi-users framework and supports non-blocking,
  async database access using SQLAlchemy’s async ORM.
- Centralizes user database access, streamlining how other microservices or application
  components interact with persistent user records.

Key Features:
-------------
- **Async Session Management:** Utilizes async SQLAlchemy sessions for high-concurrency
  and scalable service operations, crucial for modern microservices deployments.
- **Integration with FastAPI-Users:** Returns a properly configured user database object,
  enabling plug-and-play compatibility with authentication routers, managers, and
  service layers.
- **Separation of Concerns:** Abstracts away direct ORM configuration from route handlers
  and services, encouraging a clean, testable, and maintainable architecture.
- **Dependency Injection Ready:** Designed for FastAPI’s dependency system, providing
  type-safe, reusable user DB access for authentication, registration, and user management APIs.

Usage:
------
Injected wherever user persistence operations are required, especially in routes and logic
dealing with registration, authentication, or user profile management in a stateless,
service-oriented design.

Dependencies:
-------------
- fastapi-users-db-sqlalchemy
- SQLAlchemy (async ORM)
- FastAPI
- Project configuration (for DB connection/session)
- Project’s User model

"""

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
