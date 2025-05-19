from abc import ABC, abstractmethod
from typing import Any

class AgentPort(ABC):
    @abstractmethod
    async def ask(self, query: str) -> Any:
        ...