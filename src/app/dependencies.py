"""
dependencies.py

This module defines dynamic, reusable dependency injection providers for a microservices-oriented FastAPI application. 
It enables secure, configuration-driven, and user-context-aware access to core AI, retrieval, and user-related services,
paving the way for scalable, maintainable, and cloud-native architectures.

Overview:
---------
- Centralizes all core dependency construction for LLM, embedding, search, agent, and user services.
- Integrates with provider registries and project-wide settings, ensuring adapters can be swapped easily via configuration—critical for microservice extensibility, testing, or multi-provider strategies.
- Manages per-user credential injection (e.g., API keys), seamless FastAPI dependency chaining, and Jinja2 template environment setup for advanced prompt engineering in generative workflows.

Key Features:
-------------
- **Pluggable Adapters:** Selects service and API adapters at runtime based on application config and user context, enabling flexible upgrades, support for multiple providers, and easy A/B testing.
- **User-context Security:** Injects secrets (like API keys) from authenticated/verified users only, enforcing access control and proper authorization boundaries in distributed systems.
- **Session & Resource Lifecycles:** Properly manages database sessions and tool connections, ensuring resources are initialized and closed under error-checked, async-safe conditions.
- **Prompt Engine Integration:** Central management of prompt templates via Jinja2 for RAG, agent, and summarization pipelines.
- **Exception Handling:** Raises appropriate HTTP errors for missing credentials, unknown providers, or connection failures—ensuring clear communication to API clients and aiding in secure microservice orchestration.

Intended Usage:
---------------
- Use as the single import source for service dependencies (e.g., LLMService, UserService, AgentService) in FastAPI routers, background jobs, and business services.
- Ensures all user-specific context, provider choice, and connection logic is captured in one place, enforcing DRY patterns and maintainability best practices.

Dependencies:
-------------
- FastAPI (for dependency injection)
- Jinja2 (for templating)
- Project service abstractions, provider registries, and settings
- Secure user authentication from fastapi-users

Security & Best Practices:
--------------------------
- All AI/retrieval/service classes are instantiated with the correct credentials for the requesting user, strongly limiting horizontal privilege escalation.
- Error handling and logging (with traceback) are built-in for visibility into dependency instantiation failures.

"""


import os
import traceback
from typing import List

from fastapi import Depends, HTTPException, status
from jinja2 import Environment, FileSystemLoader

from app.config                         import settings
from app.db.core                        import get_db
from app.models                         import User
from app.adapters.tavily_search_adapter import TavilySearchAdapter
from app.ports.llm_port                 import LLMPort
from app.ports.user_repository_port     import UserRepositoryPort
from app.registry                       import (
    LLM_PROVIDERS,
    EMBEDDING_PROVIDERS,
    USER_REPOSITORY_PROVIDERS,
    TOOL_PROVIDERS,
)

# FASTAPI-USERS DEPENDENCIES
from app.auth.router import fastapi_users
# “active+verified” ensures is_active=True AND is_verified=True
current_verified = fastapi_users.current_user(active=True, verified=True)


from app.services.user_service            import UserService
from app.services.llm_service             import LLMService
from app.services.tavily_summarize_service import TavilySummaryService
from app.ports.agent_port                 import AgentPort
from app.adapters.agents_adapter          import AgentsAdapter
from app.services.agent_service           import AgentService


def get_llm_provider(
    current_user: User = Depends(current_verified),
) -> LLMPort:
    """
    Retrieve the appropriate LLM provider adapter based on settings and user credentials.

    Args:
        current_user (User): The currently authenticated and verified user.

    Returns:
        LLMPort: An instance of the selected LLM provider adapter.

    Raises:
        HTTPException: If the provider is unknown or no API key is available.
    """

    provider_key = settings.llm_provider
    AdapterCls  = LLM_PROVIDERS.get(provider_key)
    if not AdapterCls:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unknown LLM provider '{provider_key}'"
        )

    api_key = current_user.openai_api_key
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
    """
    Provide an instance of LLMService using the specified LLM provider.

    Args:
        llm_provider (LLMPort): The selected large language model provider.

    Returns:
        LLMService: An initialized LLM service instance.
    """

    return LLMService(llm_provider)


def get_embedding_provider():
    """
    Retrieve an instance of the configured embedding provider adapter.

    Returns:
        An instance of the selected embedding provider adapter.
    """

    AdapterCls = EMBEDDING_PROVIDERS[settings.embedding_provider]
    return AdapterCls()


async def get_user_repository(db=Depends(get_db)) -> UserRepositoryPort:
    """
    Asynchronously retrieve an instance of the configured user repository.

    Args:
        db: Database dependency returned from get_db.

    Returns:
        UserRepositoryPort: An instance of the selected user repository.
    """

    RepoCls = USER_REPOSITORY_PROVIDERS[settings.user_repository]
    return RepoCls(db)


def get_user_service(
    repo=Depends(get_user_repository),
) -> UserService:
    """
    Provide a UserService instance using the specified user repository.

    Args:
        repo: The user repository instance used for data operations.

    Returns:
        UserService: An initialized user service instance.
    """

    return UserService(repo)


def get_prompt_env() -> Environment:
    """
    Create and return a Jinja2 Environment for loading prompt templates.

    Returns:
        Environment: A Jinja2 Environment configured to load templates
                     from the 'prompts' directory without autoescaping.
    """

    templates_dir = os.path.join(os.path.dirname(__file__), "prompts")
    return Environment(
        loader=FileSystemLoader(templates_dir),
        autoescape=False,
    )


def get_tavily_adapter(
    current_user: User = Depends(current_verified),
) -> TavilySearchAdapter:
    """
    Retrieve a Tavily search adapter using the current user's API key.

    Args:
        current_user (User): The currently authenticated and verified user.

    Returns:
        TavilySearchAdapter: An initialized Tavily search adapter instance.

    Raises:
        HTTPException: If the user does not have a Tavily API key set.
    """

    if not current_user.tavily_api_key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No Tavily API key set for this user."
        )

    return TavilySearchAdapter(
        base_url=settings.tavily_base_url,
        api_key=current_user.tavily_api_key,
    )


def get_tavily_summary_service(
    llm: LLMService  = Depends(get_llm_service),
    env: Environment = Depends(get_prompt_env),
) -> TavilySummaryService:
    """
    Provide a TavilySummaryService instance using the specified LLM and template environment.

    Args:
        llm (LLMService): The large language model service instance.
        env (Environment): The Jinja2 environment for prompt templates.

    Returns:
        TavilySummaryService: An initialized Tavily summary service.
    """

    return TavilySummaryService(llm, env)


async def get_agent_adapter(
    current_user: User = Depends(current_verified),
    env: Environment  = Depends(get_prompt_env),
) -> AgentPort:
    """
    Asynchronously construct and return an agent adapter configured with user credentials and available tools.

    Args:
        current_user (User): The currently authenticated and verified user.
        env (Environment): The Jinja2 environment for loading prompt templates.

    Returns:
        AgentPort: An initialized agent adapter with configured MCP servers and instructions.

    Raises:
        HTTPException: If no OpenAI API key is available, a tool provider is unknown, 
                       or connection to a tool provider fails.
    """

    api_key = current_user.openai_api_key
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No OpenAI API key available for agent."
        )

    # build your MCP servers…
    mcp_servers = []
    for key in settings.tool_providers:
        factory = TOOL_PROVIDERS.get(key)
        if not factory:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unknown tool provider '{key}'"
            )
        mcp = factory(settings, current_user)
        if hasattr(mcp, "connect"):
            try:
                await mcp.connect()
            except Exception as e:
                tb = traceback.format_exc()
                print(f"Failed to connect to tool '{key}':\n{tb}")
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=f"Could not connect to tool '{key}': {e}"
                )
        mcp_servers.append(mcp)

    template = env.get_template("agent_instructions.jinja2")
    instructions = template.render(
        tool_providers=settings.tool_providers,
    )

    return AgentsAdapter(
        openai_api_key=current_user.openai_api_key,
        mcp_servers=mcp_servers,
        instructions=instructions,
    )


def get_agent_service(
    adapter: AgentPort = Depends(get_agent_adapter)
) -> AgentService:
    """
    Provide an AgentService instance using the specified agent adapter.

    Args:
        adapter (AgentPort): The agent adapter used for agent operations.

    Returns:
        AgentService: An initialized agent service instance.
    """
    
    return AgentService(adapter)
