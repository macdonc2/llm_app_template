"""
schemas.py

This module defines Pydantic data models (schemas) for API validation and serialization in a
microservices-based FastAPI application. The schemas in this file provide strongly typed request
and response contracts for user authentication, API key management, AI agent interaction,
retrieval-augmented generation (RAG) workflows, and search/summarization pipelines.

Overview:
---------
- Builds on top of FastAPI-Users' standard user schemas, extending to support user-level API keys for third-party service integration (e.g., OpenAI, Tavily).
- Encapsulates all request and response validation for domain endpoints, supporting reliable, auto-documented OpenAPI contracts and robust input/output checking across microservices.
- Used as a common dependency boundary between routers, service layers, and domain/business logic, promoting clean, maintainable, and type-safe design.

Key Features:
-------------
- **User Management Schemas:** UserRead, UserCreate, UserUpdate schemas allow for transparent API key handling and extension of auth features at the schema layer.
- **Token and Security Schemas:** Token and TokenData withstand changes in JWT or OAuth2 security implementations, supporting decoupled and flexible authentication flows.
- **Summarization and RAG:** Defines input/output structures (SummarizeRequest, SummarizeResponse, ContextItem) ensuring repeatable, well-typed RAG and summarization pipelines.
- **AI Agent Interaction:** AgentRequest and AgentResponse provide clear models for conversational/agent endpoints, supporting generic, AI-driven microservices.
- **ORM Compatibility:** UserRead and related models use `orm_mode = True` to allow seamless integration with SQLAlchemy ORM objects and database result sets.

Usage:
------
- Use as request/response models in FastAPI routers and OpenAPI docs.
- Pass instances between microservice layers without losing type safety or validation guarantees.
- Extend as business logic, providers, or microservices evolve, maintaining backwards-compatible APIs.

Dependencies:
-------------
- Pydantic (for schema modeling and data validation)
- FastAPI-Users (base schemas for user models)
- Python uuid and typing libraries

Security & Best Practices:
--------------------------
- All tokens and API keys are handled as optional, supporting per-user, secrets-managed architectures.
- Data validation is strictly enforced at the boundary between client/route handler and business/service logic.

"""

import uuid
from typing import List, Optional
from pydantic import BaseModel
from fastapi_users import schemas as _fu_schemas

# Use UUID as the primary key type
ID = uuid.UUID

class UserRead(_fu_schemas.BaseUser[ID]):
    """
    Schema for reading user information, including optional API keys.

    Attributes:
        openai_api_key (Optional[str]): The user's OpenAI API key, if set.
        tavily_api_key (Optional[str]): The user's Tavily API key, if set.
    """

    openai_api_key: Optional[str] = None
    tavily_api_key: Optional[str] = None
    firecrawl_api_key: Optional[str] = None

    class Config:
        orm_mode = True

class UserCreate(_fu_schemas.BaseUserCreate):
    """
    Schema for creating a new user, allowing optional API keys to be set.

    Attributes:
        openai_api_key (Optional[str]): The user's OpenAI API key (optional).
        tavily_api_key (Optional[str]): The user's Tavily API key (optional).
    """

    openai_api_key: Optional[str] = None
    tavily_api_key: Optional[str] = None
    firecrawl_api_key: Optional[str] = None

class UserUpdate(_fu_schemas.BaseUserUpdate):
    """
    Schema for updating a user's information, including optional API keys.

    Attributes:
        openai_api_key (Optional[str]): The user's OpenAI API key (optional).
        tavily_api_key (Optional[str]): The user's Tavily API key (optional).
    """

    openai_api_key: Optional[str] = None
    tavily_api_key: Optional[str] = None
    firecrawl_api_key: Optional[str] = None

class Token(BaseModel):
    """
    Schema representing an authentication token.

    Attributes:
        access_token (str): The JWT or access token string.
        token_type (str): The type of token. Defaults to "bearer".
    """

    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """
    Schema representing the payload data within a token.

    Attributes:
        sub (Optional[str]): The subject of the token, usually the user identifier.
    """

    sub: Optional[str] = None

class SummarizeRequest(BaseModel):
    """
    Request schema for summarization, specifying the search query and number of results.

    Attributes:
        query (str): The user's search query.
        top_k (int): The maximum number of search results to consider for summarization. Defaults to 5.
    """

    query: str
    top_k: int = 5

class ContextItem(BaseModel):
    """
    Schema representing a context item for summarization results.

    Attributes:
        title (str): The title of the context item.
        url (str): The source URL of the context item.
        raw_content (Optional[str]): The raw content or excerpt for context (optional).
    """

    title: str
    url: str
    raw_content: Optional[str] = None

class SummarizeResponse(BaseModel):
    """
    Response schema for summarization results.

    Attributes:
        summary (str): The generated summary text.
        expanded_query (str): The expanded or refined search query.
        contexts (List[ContextItem]): The list of context items used for summarization.
    """

    summary: str
    expanded_query: str
    contexts: List[ContextItem]

class AgentRequest(BaseModel):
    """
    Request schema for submitting a query to an agent.

    Attributes:
        query (str): The user's query to be processed by the agent.
    """

    query: str

class AgentResponse(BaseModel):
    """
    Response schema for returning an agent's answer to a query.

    Attributes:
        response (str): The answer or response generated by the agent.
    """
    
    response: str
