from typing import List
from jinja2 import Environment
from app.ports.tavily_search_port import TavilySearchPort
from app.services.llm_service import LLMService

class TavilyService:
    """
    Service class for performing search and summarization with Tavily and an LLM.

    This class combines search results with prompt templating to generate summaries
    using a large language model (LLM).

    Attributes:
        adapter (TavilySearchPort): The Tavily search adapter for retrieving documents.
        llm (LLMService): The LLM service for generating drafts and summaries.
        search_tpl: The Jinja2 template for formulating search prompts.
        summary_tpl: The Jinja2 template for summarization prompts.

    Methods:
        search_and_summarize(query: str, top_k: int = 5) -> str:
            Asynchronously retrieve, draft, and summarize relevant documents for a query.
    """

    def __init__(
        self,
        adapter: TavilySearchPort,
        llm: LLMService,
        prompt_env: Environment,
    ):
        """
        Initialize the TavilyService with a search adapter, LLM service, and prompt environment.

        Args:
            adapter (TavilySearchPort): The Tavily search adapter instance.
            llm (LLMService): The LLM service instance.
            prompt_env (Environment): The Jinja2 environment for loading prompt templates.
        """

        self.adapter = adapter
        self.llm = llm
        self.search_tpl = prompt_env.get_template("tavily/search_query.jinja2")
        self.summary_tpl = prompt_env.get_template("tavily/summarization.jinja2")

    async def search_and_summarize(self, query: str, top_k: int = 5) -> str:
        """
        Perform a search and then generate a summary for the retrieved documents.

        This function:
         1. Retrieves relevant documents via Tavily.
         2. Uses an LLM to draft a summary prompt from the search results.
         3. Uses an LLM to generate the final summary from the draft.

        Args:
            query (str): The user's search query.
            top_k (int, optional): The number of top documents to retrieve. Defaults to 5.

        Returns:
            str: The summarized output based on the retrieved documents.
        """
        
        # 1) Retrieve docs
        docs: List[str] = await self.adapter.search(query, top_k)

        # 2) First LLM pass: craft prompt
        prompt1 = self.search_tpl.render(query=query, top_k=top_k, docs=docs)
        draft = await self.llm.chat_completion(prompt1)

        # 3) Second LLM pass: summarize
        prompt2 = self.summary_tpl.render(query=query, docs=[draft])
        summary = await self.llm.chat_completion(prompt2)

        return summary
