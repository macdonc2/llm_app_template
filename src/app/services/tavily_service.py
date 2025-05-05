from typing import List
from jinja2 import Environment
from app.ports.tavily_search_port import TavilySearchPort
from app.services.llm_service import LLMService

class TavilyService:
    def __init__(
        self,
        adapter: TavilySearchPort,
        llm: LLMService,
        prompt_env: Environment,
    ):
        self.adapter = adapter
        self.llm = llm
        self.search_tpl = prompt_env.get_template("tavily/search_query.jinja2")
        self.summary_tpl = prompt_env.get_template("tavily/summarization.jinja2")

    async def search_and_summarize(self, query: str, top_k: int = 5) -> str:
        # 1) Retrieve docs
        docs: List[str] = await self.adapter.search(query, top_k)

        # 2) First LLM pass: craft prompt
        prompt1 = self.search_tpl.render(query=query, top_k=top_k, docs=docs)
        draft = await self.llm.chat_completion(prompt1)

        # 3) Second LLM pass: summarize
        prompt2 = self.summary_tpl.render(query=query, docs=[draft])
        summary = await self.llm.chat_completion(prompt2)

        return summary
