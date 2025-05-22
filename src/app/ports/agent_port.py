"""
agent_port.py

This module defines the abstract agent port interface for a microservices-based FastAPI
application. The AgentPort establishes a clear contract for implementing agent adapters,
promoting loose coupling and maximum flexibility when integrating conversational AI or
agent-like backend services.

Overview:
---------
- Contains the `AgentPort` abstract base class, specifying the asynchronous `ask` method signature.
- Designed for use with the ports-and-adapters (hexagonal) architecture common in microservices—
  adapters implementing this interface can be easily swapped, mocked, or extended, supporting
  both internal and external agent implementations (e.g., OpenAI, Rasa, in-house logic).

Key Features:
-------------
- **Adapter Abstraction:** Enables microservices to interact with agent backends via a
  clean interface, regardless of implementation details or external dependencies.
- **Async Ready:** The `ask` method is asynchronous, supporting high-throughput, non-blocking
  interactions in distributed apps.
- **Extensible:** New adapters for additional agent backends can be added by subclassing
  AgentPort, enhancing maintainability and testability.
- **Clear Contract:** Encourages explicit, type-safe interface design for anyone creating
  or consuming agent adapters within the service ecosystem.

Intended Usage:
---------------
- As a dependency in FastAPI services, routes, or other microservices that need to process
  queries using agent logic, while remaining agnostic to the specific backend implementation.
- Supports dependency inversion, service composition, and mocking in tests.

Dependencies:
-------------
- Python standard library: abc, typing (no external requirements)

"""

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