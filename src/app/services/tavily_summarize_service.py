"""
tavily_summarize_service.py

This module defines the TavilySummaryService, a high-level orchestration class for expanding queries
and generating contextual summaries with a large language model (LLM), tailored for microservices-based
FastAPI architectures.

Overview:
---------
- Implements a service layer that chains prompt-based transform and aggregation: it first expands natural-language
  queries to broaden recall, and then synthesizes concise summaries over retrieved context using AI.
- Leverages dependency injection for both the LLM provider and the Jinja2 template environment, allowing for
  testability, extendibility, and portability across evolving AI/microservice stacks.
- Integrates seamlessly into retrieval-augmented generation (RAG) or advanced semantic search workflows.

Key Features:
-------------
- **Composable AI Workflows:** Separates and modularizes query expansion and summarization, making it easy to
  evolve or substitute prompt templates, logic, or LLM adapters without core changes.
- **Prompt-Driven Architecture:** Templates for both expansion and summarization are loaded and filled via Jinja2,
  supporting non-engineers in rapid prompt engineering cycles for optimal results.
- **Async-Ready:** Designed for asynchronous, high-concurrency apps; methods return promptly for scalable
  deployments and are compatible with FastAPI or background jobs.
- **Adapter-Based LLM Integration:** Works with any underlying LLM provider implementing the required interface,
  facilitating swap-in for new or custom AI models as microservices evolve.

Intended Usage:
---------------
- Inject as a business logic/service dependency in FastAPI endpoints or orchestrator tasks where AI-enhanced
  summarization, report generation, or intelligent search are needed.
- Use in conjunction with retrieval services and search adapters for robust RAG and document processing pipelines.

Dependencies:
-------------
- LLMService (for AI completion and chat)
- Jinja2 (for flexible, template-driven prompt construction)
- Python standard library typing (for clear type contracts)

Security and Microservices Best Practices:
-----------------------------------------
- Stateless by design; all dependencies are injected and outputs are pure, supporting cloud-native scaling,
  CI/CD, and robust testing strategies.
- Promotes code/data separation for AI prompts and core business logic.

"""

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
