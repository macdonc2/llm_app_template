from fastapi import APIRouter, Depends
from ..schemas import UserCreate, UserRead, UserUpdate
from ..services.user_service import UserService
from ..dependencies import get_user_repository
from ..security import get_current_user, hash_password

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserRead, status_code=201)
async def register_user(user_in: UserCreate, repo=Depends(get_user_repository)):
    service = UserService(repo)
    return await service.create_user(user_in)

@router.get("/me", response_model=UserRead)
async def read_users_me(current_user=Depends(get_current_user)):
    return current_user

@router.patch("/me", response_model=UserRead)
async def update_profile(update: UserUpdate, repo=Depends(get_user_repository), current_user=Depends(get_current_user)):
    if update.email:
        current_user.email = update.email
    if update.password:
        current_user.hashed_password = hash_password(update.password)
    repo.db.add(current_user)
    await repo.db.commit()
    await repo.db.refresh(current_user)
    return current_user
