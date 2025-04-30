from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    open_ai_api_key: Optional[str] = None

class UserRead(BaseModel):
    id: str
    email: EmailStr
    created_at: datetime
    open_ai_api_key: Optional[str] = None

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    sub: str | None = None

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = None
    open_ai_api_key: Optional[str] = None
