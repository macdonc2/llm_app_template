from abc import ABC, abstractmethod

class EmbeddingPort(ABC):
    @abstractmethod
    async def embed_query(self, text: str) -> list[float]:
        ...
