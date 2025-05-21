from abc import ABC, abstractmethod
from typing import List

class TavilySearchPort(ABC):
    """
    Abstract base class defining the interface for Tavily search adapters.

    Methods:
        search(query: str, top_k: int = 5) -> List[str]:
            Asynchronously perform a search with the specified query and return the top results.
    """
    @abstractmethod
    async def search(self, query: str, top_k: int = 5) -> List[str]:
        """
        Asynchronously perform a search and retrieve the top results.

        Args:
            query (str): The search query string.
            top_k (int, optional): The maximum number of top results to return. Defaults to 5.

        Returns:
            List[str]: The list of search results matching the query.
        """
        ...
