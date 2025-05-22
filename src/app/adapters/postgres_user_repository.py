"""
postgres_user_repository.py

This module provides a concrete implementation of the UserRepositoryPort for a microservices-based FastAPI application using PostgreSQL as the data store with SQLAlchemy's async ORM support.

Overview:
---------
The `PostgresUserRepository` class serves as the adapter between the domain-driven user logic and the PostgreSQL database, facilitating the persistence, retrieval, and update of User entities. By implementing the `UserRepositoryPort` interface, this repository allows for loose coupling and easy swapping of persistence mechanisms, a common best practice in microservices architectures.

Key Functions:
--------------
- **create_user**: Persists a new user with proper password hashing and unique identifier generation. Handles database integrity errors, such as duplicate email registration.
- **get_user_by_email**: Fetches user entities using an email lookup, enabling authentication and lookup services.
- **get_by_id**: Retrieves user information by unique user ID for profile or permission checks.
- **update**: Updates an existing user record in the database, typically used for password resets or profile edits.

Key Features:
-------------
- **Asynchronous ORM Integration**: Uses SQLAlchemy's async session for non-blocking I/O, ensuring scalability and responsiveness in a microservices environment.
- **Security Best Practices**: Implements salting and hashing of user passwords before storage.
- **Open for Extension**: Adheres to the ports-and-adapters (hexagonal) architecture, making it straightforward to provide additional repository implementations (e.g., for testing or alternative databases).
- **Exception Handling**: Converts DB-specific integrity errors (like duplicate users) into meaningful HTTP responses suitable for FastAPI routes.

Intended Usage:
---------------
This repository is typically injected as a dependency in FastAPI routes or service layers, supporting user registration, login, and update flows. By handling all DB-specific logic here, the microservice maintains a clear separation of concerns, aiding maintainability and testability.

Dependencies:
-------------
- SQLAlchemy async ORM
- FastAPI
- Project-specific utils: password hashing, salt generation, and domain/user schemas

"""

from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from ..ports.user_repository_port import UserRepositoryPort
from ..models import User
from ..utils import new_salt, generate_userid
from ..security import hash_password
from ..schemas import UserCreate

class PostgresUserRepository(UserRepositoryPort):
    def __init__(self, db):
        self.db = db

    async def create_user(self, user: UserCreate) -> User:
        salt = new_salt()
        user_id = generate_userid(user.email, salt)
        hashed_pw = hash_password(user.password)
        db_user = User(id=user_id, email=user.email, salt=salt, hashed_password=hashed_pw, openai_api_key=user.openai_api_key)
        self.db.add(db_user)
        try:
            await self.db.commit()
        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        await self.db.refresh(db_user)
        return db_user

    async def get_user_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
    
    async def get_by_id(self, user_id: str) -> User | None:
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def update(self, user: User) -> User:
        # assume `user` is already attached to session
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
    

