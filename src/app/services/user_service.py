class UserService:
    def __init__(self, repo):
        self.repo = repo

    async def create_user(self, user_create):
        return await self.repo.create_user(user_create)

    async def get_user_by_email(self, email: str):
        return await self.repo.get_user_by_email(email)
