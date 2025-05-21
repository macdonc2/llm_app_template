from typing import List
from jinja2 import Environment

from app.services.llm_service import LLMService

class TavilySummaryService:
    """
    Service class for expanding queries and generating summaries with an LLM.

    This class uses provided prompt templates to expand a user's query and summarize
    context information using a large language model (LLM).

    Attributes:
        llm (LLMService): The LLM service used to generate expansions and summaries.
        expansion_template: Jinja2 template for query expansion.
        summary_template: Jinja2 template for summarization.

    Methods:
        expand_query(query: str) -> str:
            Asynchronously expand a query using the expansion template and LLM.
        summarize(query: str, contexts: List[str]) -> str:
            Asynchronously summarize contexts related to a query using the summary template and LLM.
    """
     
    def __init__(self, llm: LLMService, prompt_env: Environment):
        """
        Initialize the TavilySummaryService with an LLM service and prompt environment.

        Args:
            llm (LLMService): The LLM service instance.
            prompt_env (Environment): Jinja2 environment for loading templates.
        """

        self.llm = llm
        self.expansion_template = prompt_env.get_template("tavily/expansion.jinja2")
        self.summary_template = prompt_env.get_template("tavily/summarization.jinja2")

    async def expand_query(self, query: str) -> str:
        """
        Expand the user's query using the expansion template and LLM.

        Args:
            query (str): The original user query.

        Returns:
            str: The expanded version of the query.
        """

        prompt = self.expansion_template.render(query=query)
        return await self.llm.chat(prompt)

    async def summarize(self, query: str, contexts: List[str]) -> str:
        """
        Generate a summary for the provided contexts using the summary template and LLM.

        Args:
            query (str): The original user query.
            contexts (List[str]): The list of context strings to summarize.

        Returns:
            str: The generated summary.
        """
        
        prompt = self.summary_template.render(query=query, contexts=contexts)
        return await self.llm.chat(prompt)
