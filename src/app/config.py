from pydantic import BaseSettings
from datetime import timedelta

class Settings(BaseSettings):
    database_url: str
    openai_api_key: str

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    user_salt: str

    llm_provider: str = "openai"
    embedding_provider: str = "openai"
    user_repository: str = "postgres"

    class Config:
        env_file = ".env"

settings = Settings()
