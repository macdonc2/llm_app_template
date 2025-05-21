from fastapi import APIRouter, Depends
from typing import List

from app.dependencies import get_tavily_adapter, get_tavily_summary_service
from app.ports.tavily_search_port import TavilySearchPort
from app.services.tavily_summarize_service import TavilySummaryService
from app.schemas import ContextItem, SummarizeRequest, SummarizeResponse
from app.auth.router import fastapi_users

current_active_user = fastapi_users.current_user(active=True, verified=True)

router = APIRouter(
    prefix="/tavily",
    tags=["tavily"],
    dependencies=[Depends(current_active_user)],
)


@router.post("/summarize", response_model=SummarizeResponse)
async def tavily_summarize(
    req: SummarizeRequest,
    adapter: TavilySearchPort = Depends(get_tavily_adapter),
    summarizer: TavilySummaryService = Depends(get_tavily_summary_service),
):
    """
    Generate a summary of search results for a user query.

    Expands the user's query, performs a search, and then summarizes the results.

    Args:
        req (SummarizeRequest): The request containing the query and search preferences.
        adapter (TavilySearchPort): The adapter used to perform the search.
        summarizer (TavilySummaryService): The service used to expand and summarize the query results.

    Returns:
        SummarizeResponse: A response containing the summary, expanded query, and context items.
    """
    
    expanded_query = await summarizer.expand_query(query=req.query)
    raw = await adapter.search(query=expanded_query, top_k=req.top_k)
    contexts: List[ContextItem] = [ContextItem(**ctx) for ctx in raw]

    summary_text = await summarizer.summarize(
        req.query, [c.raw_content or "" for c in contexts]
    )

    return SummarizeResponse(
        summary=summary_text,
        expanded_query=expanded_query,
        contexts=contexts,
    )
