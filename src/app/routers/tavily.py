# base_app/src/app/routers/tavily.py

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List

from app.dependencies import get_tavily_adapter, get_tavily_summary_service
from app.ports.tavily_search_port  import TavilySearchPort
from app.schemas import SummarizeRequest, SummarizeResponse
from app.services.tavily_summarize_service import TavilySummaryService

router = APIRouter(prefix="/tavily", tags=["tavily"])

@router.post("/summarize", response_model=SummarizeResponse)
async def tavily_summarize(
    req: SummarizeRequest,
    adapter: TavilySearchPort = Depends(get_tavily_adapter),
    summarizer: TavilySummaryService = Depends(get_tavily_summary_service),
):
    # 1) Fetch raw docs
    contexts: List[str] = await adapter.search(req.query, req.top_k)

    # 2) Summarize them
    summary_text: str = await summarizer.summarize(req.query, contexts)

    return SummarizeResponse(summary=summary_text, contexts=contexts)
