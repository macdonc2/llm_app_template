"""
agent.py

This module defines the agent query API endpoints for a microservices-based FastAPI application.
It exposes a secure, authenticated route for submitting user-generated queries to an underlying agent
service—typically powered by AI or LLM technology—while ensuring robust access control.

Overview:
---------
- Sets up a FastAPI router (`/agent`) with all endpoints restricted to users who are both active and verified,
  fulfilling key requirements for security and compliance in distributed, API-driven systems.
- Utilizes FastAPI dependency injection for service orchestration and loose coupling,
  aligning with microservice architectural best practices.

Key Features:
-------------
- **Strict User Authentication:** Every endpoint requires an authenticated user whose account is both active and email-verified,
  limiting access to trusted users and protecting sensitive AI/agent capabilities.
- **Agent Query Submission:** The `/agent/ask` endpoint accepts structured queries (`AgentRequest`), passes them to a pluggable agent service,
  and returns AI-generated or logic-derived responses in a standardized response schema (`AgentResponse`).
- **Service-Oriented and Extensible:** The design is modular, with agent logic abstracted in an injected service (`AgentService`),
  facilitating future enhancement, testing, or backend swaps.
- **Robust Error Handling:** All errors (other than HTTPExceptions) are caught and reported as HTTP 503 responses,
  providing resilient behavior in the face of agent service outages.

Intended Usage:
---------------
- To be included as a sub-router within the main FastAPI application, or as part of a dedicated agent/AI microservice.
- Enables the secure, auditable interface for users or downstream services to leverage advanced agent/LLM features,
  with strong access gating.

Dependencies:
-------------
- FastAPI for routing and security
- Domain and Pydantic schemas: AgentRequest, AgentResponse
- A service-layer abstraction (`AgentService`) and DI provider (`get_agent_service`)
- Integration with shared authentication system (`fastapi_users`)

Security Considerations:
------------------------
All endpoints require the requesting user to be authenticated, active, and verified, ensuring only authorized
users may access potentially sensitive or costly agent operations. Centralized error handling guards against
leakage of internal errors or stack traces.

"""

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