"""
config.py

This module centralizes configuration management for a microservices-based FastAPI application by
defining the `Settings` class, which encapsulates all environment-driven and application-level
configuration in a type-safe, declarative manner using Pydantic settings.

Overview:
---------
- Provides a single source of truth for sensitive credentials, connection strings, provider selection,
  and service-level configuration required across various microservices and application layers.
- Facilitates twelve-factor app principles by loading configuration from environment variables
  (optionally via `.env` file) for seamless deployment in containerized, cloud, or orchestrated environments.
- Supports robust, type-enforced settings validation and dependency injection throughout service
  code by exposing a strongly-typed `settings` instance.

Key Features:
-------------
- **Environment-Driven:** Loads settings from environment variables and `.env`, promoting stateless, reproducible deployments.
- **Secrets & Cryptography:** Manages cryptographic secrets, JWT token configuration, and hashing salt for core authentication and security flows.
- **Pluggable Providers:** Enables dynamic selection of LLM backends, embedding engines, repositories, and tool integrations, optimizing for agility in a microservices landscape.
- **Service Endpoints:** Centralizes URLs and connection details for internal and external services/APIs such as Tavily and MCP.
- **Template/Prompt Management:** Offers configurable paths for prompt templates, aiding prompt engineering and AI workflow tuning.

Intended Usage:
---------------
- Import and inject the `settings` object into microservice routers, service layers, adapters, and authentication backends to access consistent, centralized configuration.
- Extend this class as new features, providers, or endpoints are added to the microservices ecosystem.

Dependencies:
-------------
- pydantic-settings (for environment management and type validation)
- Python standard library: datetime (for time-based config)

Security & Best Practices:
--------------------------
- All secrets and sensitive credentials loaded from environment for strong separation of code and config.
- Encourages immutability and clear diagnostics on startup via Pydantic error reporting.

"""

from pydantic_settings import BaseSettings
from datetime import timedelta

class Settings(BaseSettings):
    """
    Application configuration settings.

    Attributes:
        database_url (str): Database connection URL.
        tavily_base_url (str): Base URL for the Tavily API.
        secret_key (str): Secret key for cryptographic operations.
        algorithm (str): JWT algorithm for token encoding. Defaults to "HS256".
        access_token_expire_minutes (int): Access token expiration time in minutes. Defaults to 60.
        user_salt (str): Salt used for user password hashing.
        prompt_path (str): Path to prompt templates. Defaults to "src/app/prompts".
        llm_provider (str): The LLM provider to use. Defaults to "openai".
        embedding_provider (str): The embedding provider to use. Defaults to "openai".
        user_repository (str): The user repository type. Defaults to "postgres".
        mcp_base_url (str): Base URL for MCP API. Defaults to "https://api.macdonml.com".
        tool_providers (list[str]): List of enabled tool providers. Defaults to ["calculator"].
    """

    database_url: str
    tavily_base_url: str  

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    user_salt: str

    prompt_path: str = "src/app/prompts"

    llm_provider: str = "openai"
    embedding_provider: str = "openai"
    user_repository: str = "postgres"

    mcp_base_url: str = "https://api.macdonml.com"
    tool_providers: list[str] = ["calculator"]

    class Config:
        env_file = ".env"

settings = Settings()
