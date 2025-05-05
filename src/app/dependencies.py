import os
from jinja2 import Environment, FileSystemLoader
from fastapi import Depends, HTTPException, status

from app.config                       import settings
from app.db                           import get_db
from app.models                       import User
from app.adapters.tavily_search_adapter import TavilySearchAdapter
from app.ports.llm_port               import LLMPort
from app.ports.user_repository_port import UserRepositoryPort
from app.registry                     import LLM_PROVIDERS, EMBEDDING_PROVIDERS, USER_REPOSITORY_PROVIDERS
from app.security                     import get_current_user
from app.services.user_service        import UserService
from app.services.llm_service         import LLMService
from app.services.tavily_summarize_service import TavilySummaryService

def get_llm_provider(
    current_user: User = Depends(get_current_user),
) -> LLMPort:
    """
    Chooses an LLMPort implementation based on settings.llm_provider,
    then instantiates it with the current user's key (or global fallback).
    """
    provider_key = settings.llm_provider  # e.g. "openai", "hf"
    AdapterCls = LLM_PROVIDERS.get(provider_key)
    if not AdapterCls:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unknown LLM provider '{provider_key}'"
        )

    # per-user first, then global
    api_key = current_user.openai_api_key or settings.openai_api_key
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No API key available for LLM."
        )

    # Adapter constructors may differ by provider
    if provider_key == "hf":
        # e.g. HuggingFace adapter expects a model name
        return AdapterCls(settings.hf_model_name)
    return AdapterCls(api_key=api_key)


def get_llm_service(
    llm_provider: LLMPort = Depends(get_llm_provider),
) -> LLMService:
    """
    Wraps an LLMPort in your LLMService, which exposes `chat()`.
    """
    return LLMService(llm_provider)


def get_embedding_provider():
    """
    Instantiates your embedding adapter based on settings.embedding_provider.
    """
    AdapterCls = EMBEDDING_PROVIDERS[settings.embedding_provider]
    return AdapterCls()


async def get_user_repository(db=Depends(get_db)) -> UserRepositoryPort:
    """
    Instantiates your user repository (e.g. Postgres) for UserService.
    """
    RepoCls = USER_REPOSITORY_PROVIDERS[settings.user_repository]
    return RepoCls(db)


def get_user_service(
    repo = Depends(get_user_repository),
) -> UserService:
    """
    Wraps your user repo in the UserService.
    """
    return UserService(repo)


def get_prompt_env() -> Environment:
    """
    Jinja2 environment pointed at src/app/prompts/
    """
    templates_dir = os.path.join(os.path.dirname(__file__), "prompts")
    return Environment(loader=FileSystemLoader(templates_dir))


def get_tavily_adapter(
    user: User = Depends(get_current_user),
) -> TavilySearchAdapter:
    """
    Instantiates the TavilySearchAdapter with the per-user key.
    """
    if not user.tavily_api_key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No Tavily API key set for this user."
        )
    return TavilySearchAdapter(
        base_url=settings.tavily_base_url,
        api_key=user.tavily_api_key,
    )


def get_tavily_summary_service(
    llm: LLMService    = Depends(get_llm_service),
    env: Environment   = Depends(get_prompt_env),
) -> TavilySummaryService:
    """
    Provides the TavilySummaryService, which only needs LLMService + templates.
    """
    return TavilySummaryService(llm, env)
