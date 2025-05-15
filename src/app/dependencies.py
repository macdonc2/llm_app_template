import os
from typing import List
from jinja2 import Environment, FileSystemLoader
from fastapi import Depends, HTTPException, status

from app.config                            import settings
from app.db                                import get_db
from app.models                            import User
from app.adapters.tavily_search_adapter    import TavilySearchAdapter
from app.ports.llm_port                    import LLMPort
from app.ports.user_repository_port        import UserRepositoryPort
from app.registry                          import (
    LLM_PROVIDERS,
    EMBEDDING_PROVIDERS,
    USER_REPOSITORY_PROVIDERS,
    TOOL_PROVIDERS,
)
from app.security                          import get_current_user
from app.services.user_service             import UserService
from app.services.llm_service              import LLMService
from app.services.tavily_summarize_service import TavilySummaryService

from app.ports.agent_port                  import AgentPort
from app.adapters.agents_adapter           import AgentsAdapter
from app.services.agent_service            import AgentService


def get_llm_provider(
    current_user: User = Depends(get_current_user),
) -> LLMPort:
    provider_key = settings.llm_provider
    AdapterCls  = LLM_PROVIDERS.get(provider_key)
    if not AdapterCls:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unknown LLM provider '{provider_key}'"
        )

    api_key = current_user.openai_api_key or settings.openai_api_key
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No API key available for LLM."
        )

    if provider_key == "hf":
        return AdapterCls(settings.hf_model_name)
    return AdapterCls(api_key=api_key)


def get_llm_service(
    llm_provider: LLMPort = Depends(get_llm_provider),
) -> LLMService:
    return LLMService(llm_provider)


def get_embedding_provider():
    AdapterCls = EMBEDDING_PROVIDERS[settings.embedding_provider]
    return AdapterCls()


async def get_user_repository(db=Depends(get_db)) -> UserRepositoryPort:
    RepoCls = USER_REPOSITORY_PROVIDERS[settings.user_repository]
    return RepoCls(db)


def get_user_service(
    repo=Depends(get_user_repository),
) -> UserService:
    return UserService(repo)


def get_prompt_env() -> Environment:
    templates_dir = os.path.join(os.path.dirname(__file__), "prompts")
    return Environment(loader=FileSystemLoader(templates_dir))


def get_tavily_adapter(
    user: User = Depends(get_current_user),
) -> TavilySearchAdapter:
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
    llm: LLMService  = Depends(get_llm_service),
    env: Environment = Depends(get_prompt_env),
) -> TavilySummaryService:
    return TavilySummaryService(llm, env)


async def get_agent_adapter(
    current_user: User = Depends(get_current_user)
) -> AgentPort:
    """
    Builds an AgentsAdapter that wraps:
      - the user’s OpenAI key
      - a list of MCPServerSse tool clients for each provider in settings.tool_providers
    """
    # 1) Determine the user’s OpenAI API key (per-user or global)
    api_key = current_user.openai_api_key or settings.openai_api_key
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No OpenAI API key available for agent."
        )

    # 2) Instantiate and connect each MCPServerSse client
    mcp_servers: List[object] = []
    for key in settings.tool_providers:  # e.g. ["calculator","web_search","rag"]
        factory = TOOL_PROVIDERS.get(key)
        if not factory:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unknown tool provider '{key}'"
            )
        mcp = factory(settings)
        # ensure the SSE stream is opened before use
        if hasattr(mcp, "connect"):
            try:
                await mcp.connect()
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=f"Could not connect to tool '{key}': {e}"
                )
        mcp_servers.append(mcp)

    # 3) Return the unified AgentsAdapter
    return AgentsAdapter(
        openai_api_key=api_key,
        mcp_servers=mcp_servers,  # match AgentsAdapter.__init__
        instructions=(
            "You have access to multiple tools: calculator, web search, RAG, etc. "
            "Invoke them when needed; otherwise answer directly."
        )
    )


def get_agent_service(
    adapter: AgentPort = Depends(get_agent_adapter)
) -> AgentService:
    return AgentService(adapter)
