from fastapi import Depends
from .config import settings
from .db import get_db
from .registry import LLM_PROVIDERS, EMBEDDING_PROVIDERS, USER_REPOSITORY_PROVIDERS
from .security import get_current_user
from .services.user_service import UserService

def get_llm_provider(
        current_user = Depends(get_current_user),
):
    key = current_user.openai_api_key
    cls = LLM_PROVIDERS[settings.llm_provider]
    return cls(api_key=key)

def get_embedding_provider():
    cls = EMBEDDING_PROVIDERS[settings.embedding_provider]
    return cls()

async def get_user_repository(db=Depends(get_db)):
    cls = USER_REPOSITORY_PROVIDERS[settings.user_repository]
    return cls(db)

def get_user_service(
    repo = Depends(get_user_repository),
) -> UserService:
    return UserService(repo)