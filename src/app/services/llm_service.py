"""
llm_service.py

This module defines the LLMService class, which acts as a high-level service layer for interacting with large language model (LLM) providers in a microservices-based FastAPI application. By using an injected adapter conforming to the LLMPort interface, this service enables loosely coupled, extensible, and testable integration of LLM-powered features across microservices.

Overview:
---------
- Implements the `LLMService` class, which encapsulates the business logic for generating natural language responses from LLMs.
- Follows the ports-and-adapters (hexagonal) architecture, allowing seamless swapping, mocking, or expansion of LLM providers such as OpenAI, local deployments, or cloud-based APIs.
- Ensures all communications with the LLM backend are asynchronous, supporting high-throughput and concurrent microservices architectures.

Key Features:
-------------
- **Adapter-Based Design:** Utilizes the LLMPort interface, so any compliant adapter can be injected (OpenAI, private LLM, etc.), supporting future-proofing and easy provider migration.
- **Async Execution:** The `chat` method is asynchronous, enabling efficient integration with FastAPI endpoints and background processes in distributed environments.
- **Simplicity and Encapsulation:** The service presents a single, high-level `chat` method for domain or API usage, abstracting away infrastructure specifics from the calling code.
- **Testability:** Easily mockable for unit and integration tests by injecting a custom or fake LLMPort instance.

Usage:
------
- Injected in FastAPI route functions, background jobs, or orchestrating services to provide core language generation capabilities.
- Serves as a façade/facilitator between domain logic and potentially complex, external LLM APIs.

Dependencies:
-------------
- The abstract `LLMPort` interface (for adapter injection).

Security and Best Practices:
---------------------------
- Keeps API/controller layers decoupled from LLM provider implementation and credentials.
- Enables safe scaling and distribution of text-generation workloads in stateless service deployments.

"""

from app.ports.llm_port import LLMPort

class LLMService:
    """
    Service class for interacting with a large language model (LLM) adapter.

    This class provides methods to communicate with the underlying LLM for generating responses.

    Attributes:
        llm (LLMPort): The LLM adapter instance used for communication.

    Methods:
        chat(prompt: str) -> str:
            Asynchronously generate a response from the LLM based on the provided prompt.
    """

    def __init__(self, llm: LLMPort):
        """
        Initialize the LLMService with a specific LLM adapter.

        Args:
            llm (LLMPort): The LLM adapter instance.
        """

        self.llm = llm

    async def chat(self, prompt: str) -> str:
        """
        Asynchronously generate a response from the LLM.

        Args:
            prompt (str): The input prompt to send to the LLM.

        Returns:
            str: The generated response from the LLM.
        """
        
        return await self.llm.chat(prompt)
