from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.services.agent_service import AgentService
from app.dependencies import get_agent_service
from app.schemas import AgentRequest, AgentResponse

router = APIRouter(prefix="/agent", tags=["agent"])

@router.post("/ask", response_model=AgentResponse)
async def ask(
    req: AgentRequest,
    svc: AgentService = Depends(get_agent_service),
):
    """
    Endpoint that accepts a natural‐language query, invokes the Agent,
    and returns its response (using tools as needed).
    """
    output = await svc.ask(req.query)
    return AgentResponse(response=output)