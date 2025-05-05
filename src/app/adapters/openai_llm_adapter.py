import asyncio
from openai import OpenAI
from ..ports.llm_port import LLMPort

class OpenAILLMAdapter(LLMPort):
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.client = OpenAI(api_key=api_key)
        self.model  = model

    async def chat(self, prompt: str) -> str:
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
