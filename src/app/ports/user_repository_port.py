"""
user_repository_port.py

This module defines the abstract repository port for user data operations in a microservices-based FastAPI application. By introducing the `UserRepositoryPort` interface, it enables dependency injection and facilitates the implementation of clean, scalable, and easily testable adapters between the domain logic and data persistence layers.

Overview:
---------
- Declares the `UserRepositoryPort` abstract base class, defining the asynchronous CRUD (Create, Read, Update) contract for user data management.
- Enables the application to interact with user records without coupling to specific data storage or technology (e.g., relational DB, NoSQL, remote API).
- Follows the hexagonal (ports-and-adapters) architecture, supporting adaptability and clear separation of domain and infrastructure concerns.

Key Features:
-------------
- **Abstract CRUD Operations:** Enforces a standard interface for user creation, retrieval by email or ID, and user update, ensuring consistency across all user data sources.
- **Asynchronous Execution:** All repository methods are async, providing non-blocking, scalable I/O suitable for modern, distributed microservices ecosystems.
- **Testability and Swap-ability:** Supports mocking and fake implementations, making testing, local development, and future backend migrations straightforward.
- **Strong Typing:** Utilizes core domain schemas and models (`User`, `UserCreate`) for type safety and clarity.

Intended Usage:
---------------
- To be subclassed by concrete adapters handling real data persistence (e.g., PostgreSQL, MongoDB, external user services).
- Injected as a dependency in FastAPI endpoints, background tasks, and domain service layers that require robust user management in a microservice context.

Dependencies:
-------------
- app.models.User (the domain User model)
- app.schemas.UserCreate (Pydantic user creation schema)
- Python standard library: abc (abstract base class support)

"""

from abc import ABC, abstractmethod
from app.models import User
from app.schemas import UserCreate

class UserRepositoryPort(ABC):
    """
    Abstract base class defining the interface for user repository adapters.

    Methods:
        create_user(user: UserCreate) -> User:
            Asynchronously create a new user in the repository.

        get_user_by_email(email: str) -> User | None:
            Asynchronously retrieve a user by their email address.

        get_by_id(user_id: str) -> User | None:
            Asynchronously retrieve a user by their unique identifier.

        update(user: User) -> User:
            Asynchronously update a user's information in the repository.
    """

    @abstractmethod
    async def create_user(self, user: UserCreate) -> User:
        """
        Asynchronously create a new user.

        Args:
            user (UserCreate): The user creation data.

        Returns:
            User: The newly created user object.
        """
        ...
    
    @abstractmethod
    async def get_user_by_email(self, email: str) -> User | None:
        """
        Asynchronously retrieve a user by their email address.

        Args:
            email (str): The user's email address.

        Returns:
            User | None: The user object if found, else None.
        """
        ...
    
    @abstractmethod
    async def get_by_id(self, user_id: str) -> User | None: 
        """
        Asynchronously retrieve a user by their unique identifier.

        Args:
            user_id (str): The user's unique identifier.

        Returns:
            User | None: The user object if found, else None.
        """
        ...

    @abstractmethod
    async def update(self, user: User) -> User: 
        """
        Asynchronously update an existing user's information.

        Args:
            user (User): The user object with updated information.

        Returns:
            User: The updated user object.
        """
        ...
