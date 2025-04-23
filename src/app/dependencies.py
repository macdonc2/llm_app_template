from fastapi import Depends
from .config import settings
from .db import get_db
from .registry import LLM_PROVIDERS, EMBEDDING_PROVIDERS, USER_REPOSITORY_PROVIDERS

def get_llm_provider():
    cls = LLM_PROVIDERS[settings.llm_provider]
    return cls()

def get_embedding_provider():
    cls = EMBEDDING_PROVIDERS[settings.embedding_provider]
    return cls()

async def get_user_repository(db=Depends(get_db)):
    cls = USER_REPOSITORY_PROVIDERS[settings.user_repository]
    return cls(db)
