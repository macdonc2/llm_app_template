from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    openai_api_key: Optional[str] = None
    tavily_api_key: Optional[str] = None

class UserRead(BaseModel):
    id: str
    email: EmailStr
    created_at: datetime
    openai_api_key: Optional[str] = None
    tavily_api_key: Optional[str] = None

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
    openai_api_key: Optional[str] = None
    tavily_api_key: Optional[str] = None

class SummarizeRequest(BaseModel):
    query: str
    top_k: int = 5

class ContextItem(BaseModel):
    title: str
    url: str
    raw_content: Optional[str] = None

class SummarizeResponse(BaseModel):
    summary: str
    contexts: List[ContextItem]
