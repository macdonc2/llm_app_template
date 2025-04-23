from .adapters.openai_llm_adapter import OpenAILLMAdapter
from .adapters.openai_embedding_adapter import OpenAIEmbeddingAdapter
from .adapters.postgres_user_repository import PostgresUserRepository

LLM_PROVIDERS = {
    "openai": OpenAILLMAdapter,
}

EMBEDDING_PROVIDERS = {
    "openai": OpenAIEmbeddingAdapter,
}

USER_REPOSITORY_PROVIDERS = {
    "postgres": PostgresUserRepository,
}
