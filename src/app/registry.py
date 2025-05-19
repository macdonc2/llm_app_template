from typing import Callable
from app.config import Settings
from agents.mcp import MCPServerSse, MCPServerSseParams


from app.adapters.openai_llm_adapter       import OpenAILLMAdapter
from app.adapters.hf_llm_adapter           import HfLLMAdapter
from app.adapters.openai_embedding_adapter import OpenAIEmbeddingAdapter
from app.adapters.postgres_user_repository import PostgresUserRepository
from app.adapters.tavily_search_adapter    import TavilySearchAdapter

LLM_PROVIDERS = {
    "openai": OpenAILLMAdapter,
    "hf":      HfLLMAdapter,
}

EMBEDDING_PROVIDERS = {
    "openai": OpenAIEmbeddingAdapter,
}

USER_REPOSITORY_PROVIDERS = {
    "postgres": PostgresUserRepository,
}

TAVILY_SEARCH_PROVIDERS = {
    "default": lambda s: TavilySearchAdapter(
        base_url=s.tavily_base_url,
        api_key=s.TAVILY_API_KEY,
    )
}

TOOL_PROVIDERS: dict[str, Callable[[Settings], object]] = {
    "calculator": lambda s: MCPServerSse(
        params=MCPServerSseParams(
            url=f"{s.mcp_base_url}/calculator/sse",
        ),
        cache_tools_list=True,
        name="calculator",
    ),
}
