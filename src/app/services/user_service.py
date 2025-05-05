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