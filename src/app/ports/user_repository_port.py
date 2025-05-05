from abc import ABC, abstractmethod
from app.models import User
from app.schemas import UserCreate

class UserRepositoryPort(ABC):
    @abstractmethod
    async def create_user(self, user: UserCreate) -> User:
        ...
    
    @abstractmethod
    async def get_user_by_email(self, email: str) -> User | None:
        ...
    
    @abstractmethod
    async def get_by_id(self, user_id: str) -> User | None: 
        ...

    @abstractmethod
    async def update(self, user: User) -> User: 
        ...
