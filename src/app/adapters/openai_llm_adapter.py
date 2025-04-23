from openai import OpenAI
from ..ports.llm_port import LLMPort
from ..config import settings

class OpenAILLMAdapter(LLMPort):
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)

    async def chat(self, prompt: str) -> str:
        resp = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.choices[0].message.content
