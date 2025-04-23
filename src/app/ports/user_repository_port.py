from abc import ABC, abstractmethod
from ..models import User
from ..schemas import UserCreate

class UserRepositoryPort(ABC):
    @abstractmethod
    async def create_user(self, user: UserCreate) -> User:
        ...
    
    @abstractmethod
    async def get_user_by_email(self, email: str) -> User | None:
        ...
