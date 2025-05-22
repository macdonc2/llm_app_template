"""
embedding_port.py

This module defines the abstract embedding port interface for a microservices-based
FastAPI application. The EmbeddingPort class formalizes the contract for embedding
adapters, enabling decoupled, extensible integration of various embedding providers
(e.g., local models, cloud APIs, third-party services) within distributed systems.

Overview:
---------
- Declares the `EmbeddingPort` abstract base class with the asynchronous method `embed_query`.
- Adheres to the ports-and-adapters (hexagonal) architecture, enhancing replaceability
  and clean boundaries between domain logic and infrastructure in microservices.

Key Features:
-------------
- **Adapter Abstraction:** Provides a uniform, implementation-agnostic interface for embedding
  functions, ensuring easy swapping or extension of backend embedding strategies.
- **Async Integration:** The async `embed_query` supports non-blocking remote or compute-intensive
  embedding services, leveraging Python's async/await for high microservice throughput.
- **Composable and Testable:** Designed for dependency injection into FastAPI routes or background
  workers, making logic easy to mock for tests and safe for scalable, concurrent use.
- **Explicit Contract:** Clearly defines the expected input/output signature for any embedding adapter,
  simplifying onboarding for new contributors or teams.

Intended Usage:
---------------
- To be subclassed by concrete embedding adapters (e.g., OpenAI Embeddings, HuggingFace, custom services).
- Consumed via dependency injection by FastAPI endpoints or service layers that need text-to-vector
  capabilities (retrieval-augmented generation, vector search, etc.), while abstracting away
  backend vendor and infrastructure details.

Dependencies:
-------------
- abc (Python standard library, for abstract base classes)

"""

from abc import ABC, abstractmethod

class EmbeddingPort(ABC):
    """
    Abstract base class specifying the interface for embedding adapters.

    Methods:
        embed_query(text: str) -> list[float]:
            Asynchronously generate an embedding vector for the given text query.
    """
    
    @abstractmethod
    async def embed_query(self, text: str) -> list[float]:
        """
        Asynchronously generate an embedding vector for a text query.

        Args:
            text (str): The input text to embed.

        Returns:
            list[float]: The embedding vector representation of the input text.
        """
        ...
