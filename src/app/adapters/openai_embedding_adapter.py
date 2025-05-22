"""
openai_embedding_adapter.py

This module provides an adapter implementation for embedding text queries using OpenAI's embedding API,
specifically designed for use within a microservices-based FastAPI application.

Overview:
---------
The `OpenAIEmbeddingAdapter` bridges the application's domain logic and the external OpenAI API,
offering an asynchronous interface for generating high-quality text embeddings. By conforming to
the `EmbeddingPort` (an abstract port defined elsewhere in the hexagonal architecture), this adapter
enables seamless substitution or extension with other embedding service providers when needed.

Key Features:
-------------
- Asynchronously generates dense vector representations (embeddings) for input text, leveraging OpenAI's API.
- Abstracted behind the `EmbeddingPort` interface to promote testability, maintainability, and loose coupling between core logic and vendor-specific implementations.
- Uses configuration management to securely retrieve API credentials, supporting twelve-factor and cloud-native deployment best practices.
- Ideal for microservice deployment scenarios where vector search, semantic search, or text similarity features are required (e.g., search engines, chatbots, recommender systems, and document classifiers).

Intended Usage:
---------------
This adapter is intended to be injected as a dependency wherever vector representations of text
are required within the service. It fits naturally into the service layer of a FastAPI application, 
and can be plugged into background workers, request handlers, or any subsystem requiring semantic text analysis.

Example:
--------
    adapter = OpenAIEmbeddingAdapter()
    embedding = await adapter.embed_query("How does FastAPI support microservices?")

Dependencies:
-------------
- `openai`: OpenAI Python SDK.
- Application configuration object supplying the OpenAI API key.
- `EmbeddingPort`: Abstract interface the adapter implements.

See Also:
---------
- ports.embedding_port.EmbeddingPort: Base interface for embedding providers.
- config.settings: Application configuration for sensitive credentials.
"""


from openai import OpenAI
from ..ports.embedding_port import EmbeddingPort
from ..config import settings

class OpenAIEmbeddingAdapter(EmbeddingPort):
    """
    Adapter for embedding queries using OpenAI's embedding API.

    Utilizes the OpenAI client to generate embeddings for input texts.
    """

    def __init__(self):
        """
        Initialize the OpenAIEmbeddingAdapter.

        Sets up the OpenAI API client using the provided API key from settings.
        """

        self.client = OpenAI(api_key=settings.openai_api_key)

    async def embed_query(self, text: str) -> list[float]:
        """
        Generate an embedding vector for the given input text using OpenAI.

        Args:
            text (str): Input text to be embedded.

        Returns:
            list[float]: The embedding vector representing the input text.
        """

        resp = await self.client.embeddings.create(model="text-embedding-3-small", input=text)
        return resp.data[0].embedding
