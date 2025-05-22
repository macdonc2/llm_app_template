"""
user_service.py

This module defines the UserService class, which acts as a business logic layer 
for managing user entities in a microservices-based FastAPI architecture.
It coordinates validation, transformation, and persistence of user data while
abstracting away repository and database details from API routes and controllers.

Overview:
---------
- Implements typical user use cases: creation, lookup by email, and profile updates.
- Follows the service-layer pattern, centralizing business rules and security concerns 
  (such as password hashing and unique constraint management).
- Designed for async workflows, supporting scalable microservice deployments and non-blocking API endpoints.

Key Features:
-------------
- **Repository Abstraction:** Interacts exclusively with an injected user repository (repo), enabling 
  swap-in/swap-out of different persistence backends or mock implementations for testing.
- **Domain Model-Driven:** Accepts and returns strongly-typed domain models and schemas (`User`, `UserCreate`, `UserUpdate`),
  ensuring data integrity and predictable behavior throughout the service layer.
- **Business Logic Aggregation:** Orchestrates key concerns such as password hashing, email updates,
  API key management, and persistence, keeping routes/controllers slim and focused.
- **Extensible and Testable:** Structured for easy enhancement (e.g., add multi-factor logic, event emission) 
  and for unit/integration testing by using repository interface injection.

Usage:
------
- Inject as a dependency into FastAPI routers/handlers for all user management, profile, or account endpoints.
- Serves as the core orchestrator between API validation layers and persistence providers in a microservices ecosystem.

Dependencies:
-------------
- Pydantic schemas: UserCreate, UserUpdate
- ORM model: User
- A repository/DAO class implementing user data access
- Optional project-specific security utilities for password hashing

Security Considerations:
------------------------
- All password updates are securely hashed before saving, helping protect users’ credentials at rest.
- Business logic for other sensitive fields (e.g., API keys) can be centralized and locked-down here.

"""

from app.schemas import UserCreate, UserUpdate
from app.models import User

class UserService:
    def __init__(self, repo):
        self.repo = repo

    async def create_user(self, user_create: UserCreate) -> User:
        # forward the Pydantic model directly
        return await self.repo.create_user(user_create)

    async def get_user_by_email(self, email: str) -> User | None:
        return await self.repo.get_user_by_email(email)
    
    async def update_user(self, user_id: str, user_update: UserUpdate) -> User:
        """
        Fetches the user by ID, applies the changes from
        `user_update`, persists, and returns the updated ORM model.
        """
        user: User = await self.repo.get_by_id(user_id)
        if user_update.email is not None:
            user.email = user_update.email
        if user_update.password is not None:
            # hash here or assume already hashed
            from app.security import hash_password
            user.hashed_password = hash_password(user_update.password)
        if user_update.openai_api_key is not None:
            user.openai_api_key = user_update.openai_api_key
        if user_update.tavily_api_key is not None:
            user.tavily_api_key = user_update.tavily_api_key

        # your repository should implement `update(user)` or `save(user)`
        updated = await self.repo.update(user)
        return updated