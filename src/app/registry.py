from typing import Callable, Type

from app.adapters.openai_llm_adapter import OpenAILLMAdapter
from app.adapters.openai_embedding_adapter import OpenAIEmbeddingAdapter
from app.adapters.hf_llm_adapter import HfLLMAdapter
from app.adapters.postgres_user_repository import PostgresUserRepository
from app.adapters.tavily_search_adapter import TavilySearchAdapter
from app.ports.llm_port import LLMPort
from app.ports.tavily_search_port import TavilySearchPort
from app.config import Settings

LLM_PROVIDERS: dict[str, Type[LLMPort]] = {
    "openai": OpenAILLMAdapter,
    "hf":      HfLLMAdapter,
}

EMBEDDING_PROVIDERS = {
    "openai": OpenAIEmbeddingAdapter,
}

USER_REPOSITORY_PROVIDERS = {
    "postgres": PostgresUserRepository,
}

TAVILY_SEARCH_PROVIDERS: dict[str, Callable[[Settings], TavilySearchPort]] = {
    "default": lambda s: TavilySearchAdapter(
        base_url=s.TAVILY_BASE_URL,
        api_key=s.TAVILY_API_KEY,
    )
}