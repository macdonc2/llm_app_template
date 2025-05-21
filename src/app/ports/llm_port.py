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
