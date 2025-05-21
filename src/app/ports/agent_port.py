from abc import ABC, abstractmethod
from typing import Any

class AgentPort(ABC):
    """
    Abstract base class specifying the interface for agent adapters.

    Methods:
        ask(query: str) -> Any:
            Asynchronously process a user query and return the agent's response.
    """

    @abstractmethod
    async def ask(self, query: str) -> Any:
        """
        Asynchronously process a user query and return a response.

        Args:
            query (str): The user's input query.

        Returns:
            Any: The agent's response to the query.
        """
        ...