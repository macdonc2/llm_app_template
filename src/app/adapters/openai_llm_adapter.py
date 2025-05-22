"""
openai_llm_adapter.py

This module provides an asynchronous adapter for integrating OpenAI language models
(e.g., GPT-4o) into microservice-based FastAPI applications.

Overview
--------
- Implements the LLMPort interface for dependency-injection and clean separation of concerns.
- Encapsulates authentication and invocation logic for OpenAI language APIs.
- Exposes a coroutine (`chat`) optimized for non-blocking use within FastAPI endpoints.

Usage in a Microservices Context
-------------------------------
- This adapter allows your FastAPI-based microservice to interact with OpenAI LLMs as a plug-and-play,
  injectable dependency, enabling easy swapping of underlying LLM providers.
- It leverages Python's `asyncio` to run the blocking OpenAI API call in a thread pool, ensuring
  the event loop remains responsive and scalable in concurrent microservice deployments.
- Designed to be instantiated per-request or as a singleton for API-key-based authenticated access.

Typical Use
-----------
Instantiate and inject this adapter wherever LLM services are required:

    from app.adapters.openai_llm_adapter import OpenAILLMAdapter

    llm = OpenAILLMAdapter(api_key=API_KEY)
    response = await llm.chat("How can I help you today?")

Dependencies
------------
- openai>=1.0
- Python 3.8+ (for proper async/await and typing)
- Project-specific `LLMPort` interface abstraction

This module enables robust, scalable LLM integration in service-oriented architectures,
following best practices for code decoupling, dependency injection, and asyncio-based concurrency.
"""

import asyncio
from openai import OpenAI
from ..ports.llm_port import LLMPort

class OpenAILLMAdapter(LLMPort):
    """
    Adapter for interacting with OpenAI language models using the LLMPort interface.
    
    Args:
        api_key (str): OpenAI API key for authentication.
        model (str): Model name to use (default: 'gpt-4o-mini').
    """

    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        """
        Initialize the OpenAI client and set the model.
        
        Args:
            api_key (str): OpenAI API key.
            model (str, optional): Model name to use. Defaults to "gpt-4o-mini".
        """

        self.client = OpenAI(api_key=api_key)
        self.model  = model

    async def chat(self, prompt: str) -> str:
        """
        Send a prompt to the language model and return its response.
        
        Args:
            prompt (str): The user input to send to the LLM.
        
        Returns:
            str: The model's response text.
        """

        loop = asyncio.get_running_loop()
        # run the blocking .create() in a threadpool
        resp = await loop.run_in_executor(
            None,
            lambda: self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
            )
        )
        return resp.choices[0].message.content
