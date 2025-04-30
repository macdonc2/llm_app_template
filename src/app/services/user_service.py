from ..schemas import UserCreate
from ..models import User

class UserService:
    def __init__(self, repo):
        self.repo = repo

    async def create_user(self, user_create: UserCreate) -> User:
        # forward the Pydantic model directly
        return await self.repo.create_user(user_create)

    async def get_user_by_email(self, email: str) -> User | None:
        return await self.repo.get_user_by_email(email)