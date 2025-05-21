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
