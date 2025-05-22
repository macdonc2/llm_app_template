"""
agent_service.py

This module provides the agent service layer for a microservices-oriented FastAPI application.
It defines a high-level interface for processing user queries by delegating to pluggable agent adapters (via the AgentPort abstraction).
The service acts as an intermediary—enabling other microservice components, such as API endpoints or business services, to invoke agent logic without knowing or caring about the underlying agent backend (LLM, rule-based, cloud API, etc.).

Overview:
---------
- Implements the `AgentService` class, which wraps an injected `AgentPort` adapter and exposes asynchronous methods for issuing queries to the agent.
- Follows the hexagonal (ports-and-adapters) architecture, ensuring the service logic is decoupled from infrastructure implementation and can be easily swapped, mocked, or extended as requirements evolve.
- Supports the injection or interchanging of different agent adapter implementations, empowering future migration across agent providers or custom logic enhancements.

Key Features:
-------------
- **Adapter Abstraction:** Receives any implementation of `AgentPort`, delegating query resolution transparently.
- **Async-Ready:** Asynchronous by design, supporting high-concurrency FastAPI microservice endpoints and background workers.
- **Domain-Oriented Service:** Presents a simple, business-focused interface (`ask`) that can be orchestrated by higher-level application or orchestration code.

Intended Usage:
---------------
- Injected as a dependency in FastAPI route handlers, background jobs, or other microservices needing dialogue, completion, or agent-style logic.
- Used as a façade over complex agent APIs, encapsulating all agent-provider-specific details in the adapter.

Dependencies:
-------------
- AgentPort (abstract base class/interface for agent adapters)

Testability:
------------
- Easily unit-testable by injecting fake or mock AgentPort adapters.
- Enables full separation of concerns between API/controller logic and agent infrastructure.

"""

from app.ports.agent_port import AgentPort

class AgentService:
    """
    Service class for interacting with an agent adapter.

    This class provides a high-level interface for processing queries via the agent.

    Attributes:
        adapter (AgentPort): The agent adapter used to handle queries.

    Methods:
        ask(query: str) -> str:
            Asynchronously process a query using the agent adapter and return the response.
    """

    def __init__(self, adapter: AgentPort):
        """
        Initialize the AgentService with a specific agent adapter.

        Args:
            adapter (AgentPort): The agent adapter instance.
        """

        self.adapter = adapter

    async def ask(self, query: str) -> str:
        """
        Submit a query to the agent and retrieve the response.

        Args:
            query (str): The query string to process.

        Returns:
            str: The agent's response to the query.
        """
        
        return await self.adapter.ask(query)
