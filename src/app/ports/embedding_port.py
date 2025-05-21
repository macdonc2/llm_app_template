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
