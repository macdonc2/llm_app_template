"""
registry.py

This module implements centralized registries for service adapters, provider factories, and integration components for a microservices-based FastAPI application. It enables dynamic, configuration-driven selection of AI, embedding, user storage, search, and external tool adapters using a simple, declarative mapping approach. This is foundational for scalable, maintainable, and easily extensible microservice architectures.

Overview:
---------
- Maps logical provider names (from settings/environment) to their concrete adapter classes or factory functions for:
    * Large Language Model (LLM) adapters
    * Embedding model adapters
    * User repository backends
    * Tavily search adapters
    * Third-party/tool provider adapters (e.g., calculator)
- Facilitates plug-and-play microservice composition, allowing feature or technology upgrades, multi-cloud deployments, or A/B testing by simply modifying settings or environment variables.
- Exposes globally-importable constants for dependency injection providers, business logic, or API routes across the service mesh.

Key Features:
-------------
- **Dynamic Provider Resolution:** Adapters and tool backends are chosen at runtime based on app config, enabling flexibility, rapid prototyping, and support for multiple providers without rewriting core logic.
- **Centralized, Declarative Mapping:** All adapters and provider factories are declared in one place for transparency, manageability, and reduced risk of configuration drift.
- **Testability and Extensibility:** Easily inject mocks or swap implementations for local testing or when onboarding new cloud or on-premise tools.
- **Microservice Best Practice:** Adheres to the open/closed principle: new providers or adapters can be added with minimal code changes.

Usage:
------
- Used in dependency injection chains or service factory methods to select the correct adapter based on configuration.
- Powers dynamic, distributed architectures where different microservices, users, or routes may require different backend integrations.

Dependencies:
-------------
- Project adapters for LLM, embeddings, repositories, and tools
- Application Settings class (for runtime configuration/context)
- Standard typing for type-safe registry definitions

Security & Operations:
----------------------
- Provider selection is configuration-driven; keys and credentials should flow from secure environment/config stores, never hard-coded.
- Registry composition supports robust, maintainable production deployments with explicit visibility into all integration points.

"""

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
