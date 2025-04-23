from abc import ABC, abstractmethod

class LLMPort(ABC):
    @abstractmethod
    async def chat(self, prompt: str) -> str:
        ...
