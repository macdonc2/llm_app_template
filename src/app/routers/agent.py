from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_agent_service
from app.schemas import AgentRequest, AgentResponse
from app.services.agent_service import AgentService
from app.auth.router import fastapi_users

# Require an authenticated, active AND verified user for all /agent endpoints
current_active_verified = fastapi_users.current_user(active=True, verified=True)

router = APIRouter(
    prefix="/agent",
    tags=["agent"],
    dependencies=[Depends(current_active_verified)],
)


@router.post("/ask", response_model=AgentResponse)
async def ask_agent(
    req: AgentRequest,
    svc: AgentService = Depends(get_agent_service),
    user=Depends(current_active_verified),
):
    """
    Submit a query to the agent and return its response.

    Args:
        req (AgentRequest): The request object containing the user's query.
        svc (AgentService): Dependency-injected agent service for handling queries.
        user: The currently authenticated and verified user.

    Returns:
        AgentResponse: The response from the agent based on the query.

    Raises:
        HTTPException: If the agent service fails to handle the query.
    """
    
    try:
        result = await svc.ask(req.query)
        return AgentResponse(response=result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Agent failed with error: {e}",
        )