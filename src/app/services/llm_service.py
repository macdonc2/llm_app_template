class LLMService:
    def __init__(self, llm):
        self.llm = llm

    async def generate_answer(self, query: str, docs: list[str]) -> str:
        prompt = f"""You are a helpful assistant. Use the following context documents:
{docs}

Answer the question: {query}
"""
        return await self.llm.chat(prompt)
