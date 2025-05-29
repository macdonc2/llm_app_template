# app/src/app/registry.py

from typing import Callable, Optional
from app.config import Settings
from app.models import User

# Import the real SSE client & params from the OpenAI-Agents SDK
from agents.mcp.server import MCPServerSse, MCPServerSseParams

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
        api_key=s.tavily_api_key,
    )
}

TOOL_PROVIDERS: dict[str, Callable[[Settings, Optional[User]], object]] = {
    "calculator": lambda s, user=None: MCPServerSse(
        params=MCPServerSseParams(
            url=f"{s.mcp_base_url}/calculator/sse",
            messages_path=f"{s.mcp_base_url}/calculator/messages/",
            headers={},  # nothing special here
        ),
        cache_tools_list=True,
        name="calculator",
    ),
    "firecrawl": lambda s, user: MCPServerSse(
        params=MCPServerSseParams(
            url=f"{s.mcp_base_url}/firecrawl_api/sse",
            messages_path=f"{s.mcp_base_url}/firecrawl_api/messages/",
            headers={
                "Authorization": f"Bearer {user.firecrawl_api_key}"
            },
        ),
        cache_tools_list=True,
        name="firecrawl",
    ),
}
