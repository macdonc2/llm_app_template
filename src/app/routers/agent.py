from fastapi import APIRouter, Depends, HTTPException, status
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

    try:
        output = await svc.ask(req.query)
        return AgentResponse(response=output)
    except HTTPException:
        # re-raise any HTTPException you intentionally threw in DI or service
        raise
    except Exception as e:
        # catch anything unexpected and give a 503 with a useful message
        # (you could also log.exception(e) here)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Agent failed with error: {e}"
        )