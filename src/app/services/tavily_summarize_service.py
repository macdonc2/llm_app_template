from typing import List
from jinja2 import Environment

from app.services.llm_service import LLMService

class TavilySummaryService:
    """
    Given a user query and raw Tavily results (contexts),
    renders a Jinja2 summarization prompt and calls the LLM.
    """
    def __init__(self, llm: LLMService, prompt_env: Environment):
        self.llm = llm
        self.template = prompt_env.get_template("tavily/summarization.jinja2")

    async def summarize(self, query: str, contexts: List[str]) -> str:
        prompt = self.template.render(query=query, contexts=contexts)
        return await self.llm.chat(prompt)
