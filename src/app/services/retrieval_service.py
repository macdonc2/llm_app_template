"""
retrieval_service.py

This module defines the RetrievalService, which enables semantic search by combining vector embedding generation
with database-backed similarity search, designed specifically for a microservices-based FastAPI application.

Overview:
---------
- Encapsulates logic for retrieving the most relevant documents for a given user query using modern embedding models and efficient similarity search algorithms.
- Fits within a retrieval-augmented generation (RAG) or semantic search architecture as a reusable, injectable service layer.
- Employs a fully asynchronous workflow for high concurrency support in scalable, distributed systems.

Key Features:
-------------
- **Modular Microservice Component:** Operates as a domain service that bridges a database backend (e.g., PostgreSQL with vector support) and a pluggable embedding provider, supporting clean abstraction and loose coupling.
- **Semantic Search:** Uses embeddings to retrieve documents based on semantic similarity, enhancing user-facing search, chatbot grounding, or RAG queries in large language model (LLM) workflows.
- **Asynchronous and Scalable:** Designed for async invocation, allowing downstream FastAPI endpoints to remain non-blocking and responsive under load.
- **Configurable Results:** Supports dynamic `top-k` querying, allowing callers to customize result granularity for different use cases.

Intended Usage:
---------------
- Injected as a dependency in FastAPI routes or background workers tasked with document retrieval, semantic search, or RAG pipelines.
- Integrates seamlessly into microservices architectures, enabling composition with other components such as LLMs, summarizers, and access controllers.

Dependencies:
-------------
- An async-compatible database interface (such as asyncpg or an async SQLAlchemy engine) with support for vector similarity queries (e.g., pgvector extension).
- An embedding provider (implementing an async `embed_query` method).

Security & Scalability:
-----------------------
- Avoids exposing low-level DB logic directly to route handlers, enhancing safety.
- Designed for horizontal scaling, stateless operation, and easy adapter swap-out in a microservices ecosystem.

"""

class RetrievalService:
    """
    Service class for retrieving relevant documents based on query embeddings.

    This class handles interaction between a database and an embedding provider
    to fetch documents most relevant to a user's query.

    Attributes:
        db: The database instance for document retrieval.
        embedder: The embedding provider used to generate vector representations of queries.

    Methods:
        get_relevant_docs(query: str, k: int = 5) -> list[str]:
            Asynchronously fetch the top-k most relevant documents for a given query.
    """

    def __init__(self, db, embedder):
        """
        Initialize the RetrievalService with a database and an embedding provider.

        Args:
            db: The database instance for retrieving documents.
            embedder: The embedding provider instance for generating embeddings.
        """

        self.db = db
        self.embedder = embedder

    async def get_relevant_docs(self, query: str, k: int = 5) -> list[str]:
        """
        Retrieve the top-k most relevant documents for the provided query.

        Args:
            query (str): The user's search query.
            k (int, optional): The number of top results to return. Defaults to 5.

        Returns:
            list[str]: A list of the most relevant document contents.
        """
        
        vec = await self.embedder.embed_query(query)
        rows = await self.db.fetch(
            "SELECT content FROM documents ORDER BY embedding <-> $1 LIMIT $2",
            vec, k
        )
        return [r["content"] for r in rows]
