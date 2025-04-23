from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from ..dependencies import get_user_repository
from ..security import verify_password, create_access_token, settings
from ..schemas import Token

router = APIRouter(tags=["auth"])

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), repo=Depends(get_user_repository)):
    user = await repo.get_user_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.id}, expires_delta=timedelta(minutes=settings.access_token_expire_minutes))
    return {"access_token": access_token}
