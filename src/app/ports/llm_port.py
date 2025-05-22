"""
llm_port.py

This module defines the abstract interface (port) for integrating large language model (LLM) adapters within a microservices-based FastAPI application. The LLMPort establishes a contract for incorporating LLM capabilities, enabling distributed service architectures to interact with a variety of language model providers in a clean, decoupled, and testable manner.

Overview:
---------
- Declares the `LLMPort` abstract base class, requiring implementation of an asynchronous `chat` method.
- Encapsulates the interface for communicating with LLMs—such as OpenAI, local models, or custom deployments—within a hexagonal (ports-and-adapters) design.
- Supports microservice extensibility by allowing runtime selection or swapping of LLM backends without affecting the core application logic.

Key Features:
-------------
- **Adapter Abstraction:** Cleanly separates LLM provider logic from application and domain layers, promoting maintainability and vendor-agnostic architecture.
- **Async LLM Interaction:** The `chat` method is declared asynchronous for non-blocking, scalable LLM-only or LLM-augmented microservices.
- **Dependency Injection Ready:** Designed for injection into FastAPI routes, services, or background workers, supporting easy substitution and mocking during testing.
- **Explicit Contract:** Illustrates a clear expected interface for any service implementing LLM connectivity, aiding onboarding and cross-team collaboration.

Intended Usage:
---------------
- Subclassed by concrete adapters (e.g., OpenAIAdapter, LocalLLMAdapter) that implement the async `chat` interface.
- Consumed as an injected dependency in FastAPI endpoints, orchestrators, or backend services that require generative language capabilities.
- Facilitates composition in workflows that combine LLM output with other microservice functionalities, such as search, data transformation, or decision support.

Dependencies:
-------------
- Python standard library: abc (for abstract base classes)

"""

from abc import ABC, abstractmethod

class LLMPort(ABC):
    """
    Abstract base class defining the interface for large language model (LLM) adapters.

    Methods:
        chat(prompt: str) -> str:
            Asynchronously generate a response from the LLM based on a given prompt.
    """
    @abstractmethod
    async def chat(self, prompt: str) -> str:
        """
        Asynchronously generate a response from the LLM for the provided prompt.

        Args:
            prompt (str): The input prompt or message.

        Returns:
            str: The generated response from the LLM.
        """
        ...
