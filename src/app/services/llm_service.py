from app.ports.llm_port import LLMPort

class LLMService:
    def __init__(self, llm: LLMPort):
        self.llm = llm

    async def chat(self, prompt: str) -> str:
        return await self.llm.chat(prompt)
