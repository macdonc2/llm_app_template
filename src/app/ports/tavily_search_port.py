from abc import ABC, abstractmethod
from typing import List

class TavilySearchPort(ABC):
    @abstractmethod
    async def search(self, query: str, top_k: int = 5) -> List[str]:
        """
        Perform a Tavily search and return a list of raw document strings.
        """
        ...
