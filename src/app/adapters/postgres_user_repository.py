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
        db_user = User(id=user_id, email=user.email, salt=salt, hashed_password=hashed_pw)
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
