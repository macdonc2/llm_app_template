import asyncio
from transformers import pipeline
from app.ports.llm_port import LLMPort

class HfLLMAdapter(LLMPort):
    def __init__(self, model_name: str):
        self.pipe = pipeline("text-generation", model=model_name)

    async def chat(self, prompt: str) -> str:
        loop = asyncio.get_running_loop()
        outputs = await loop.run_in_executor(
            None,
            lambda: self.pipe(prompt, max_length=200)
        )
        return outputs[0]["generated_text"]
