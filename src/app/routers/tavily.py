# base_app/src/app/routers/tavily.py

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List

from app.dependencies import get_tavily_adapter, get_tavily_summary_service
from app.ports.tavily_search_port  import TavilySearchPort
from app.schemas import ContextItem, SummarizeRequest, SummarizeResponse
from app.services.tavily_summarize_service import TavilySummaryService

router = APIRouter(prefix="/tavily", tags=["tavily"])

@router.post("/summarize", response_model=SummarizeResponse)
async def tavily_summarize(
    req: SummarizeRequest,
    adapter: TavilySearchPort = Depends(get_tavily_adapter),
    summarizer: TavilySummaryService = Depends(get_tavily_summary_service),
):
    
    # 1) Expand query
    expanded_query: str = await summarizer.expand_query(query=req.query)

    # 2) Fetch raw docs
    contexts: List[ContextItem] = [ContextItem(**ctx) for ctx in await adapter.search(query=expanded_query, top_k=req.top_k)]
    print(f"top_k: {req.top_k}")
    print(f"len_contexts: {len(contexts)}")

    # 3) Summarize them
    summary_text: str = await summarizer.summarize(req.query, [c.raw_content or "" for c in contexts])

    return SummarizeResponse(
    summary=summary_text,
    expanded_query=expanded_query,
    contexts=contexts
)

