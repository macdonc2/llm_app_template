"""
tavily_search_port.py

This module declares the abstract interface (port) for Tavily search service integration in a microservices-based FastAPI architecture. By formalizing the `TavilySearchPort` as an abstract base class, the application enables flexible, loosely coupled adapters for external or internal search functionality.

Overview:
---------
- Defines the `TavilySearchPort` abstract base class, specifying an async `search` method and result contract.
- Follows the hexagonal (ports-and-adapters) architecture pattern to promote separation of concerns, testability, and runtime adapter swapping in distributed and scalable FastAPI microservices.

Key Features:
-------------
- **Adapter Abstraction:** Decouples search logic from application and domain layers, facilitating integration with different search providers or implementations (e.g., Tavily, local search, future APIs).
- **Asynchronous Operations:** Declares the `search` method as async to ensure non-blocking network calls and scalability—an essential property in modern cloud-native and microservice deployments.
- **Explicit Interface Contract:** Clearly communicates input, output, and behavioral expectations to implementers and consuming teams, reducing integration friction.
- **Extensible and Mockable:** Supports mocking in automated tests and easy addition of new search adapters as business requirements evolve.

Intended Usage:
---------------
- Subclassed by concrete adapters that implement search requests to Tavily or alternative backends.
- Consumed via dependency injection in FastAPI endpoints, background tasks, or services that require semantic text search without regard to the underlying provider.

Dependencies:
-------------
- Python standard library: abc (for abstract base classes), typing (for type hints)

"""

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
