"""
rag.py

This module exposes endpoints for retrieval-augmented generation (RAG) workflows
in a microservices-based FastAPI application. It enables authenticated users to
submit queries, retrieve contextually relevant documents using vector similarity,
and generate responses leveraging large language models (LLMs).

Overview:
---------
- Registers a `/rag/query` POST endpoint, protected so that only active, verified
  users may access advanced retrieval and generation features.
- Integrates multiple microservice components: a retrieval service for context
  gathering, an embedding provider for semantic search, and an LLM service for
  generative response synthesis.
- Follows dependency injection principles to maintain loose coupling between
  data storage, embeddings, and language model selection—aligning with the 
  hexagonal (ports-and-adapters) architectural pattern.

Key Features:
-------------
- **Strict Authentication:** All endpoints require the user to be authenticated,
  active, and verified, protecting advanced AI/ML services from unauthorized access.
- **Composable Retrieval + Generation Flow:** Submission of an arbitrary query returns
  high-quality, context-aware, model-generated answers, powered by chained retrieval
  and LLM orchestration.
- **Microservices Ready:** Each critical layer (DB, embeddings, LLM) is injected
  as a provider, supporting service-oriented refactoring, testing, and deployment.
- **Modular Extensibility:** The architecture allows straightforward swapping or
  scaling of retrieval, embedding, or LLM backends without touching route logic.

Usage:
------
Plug this router as a submodule in the main FastAPI app. Meant for cloud-native
deployments where document retrieval and LLM response generation are provided as
stateless, scalable API services.

Dependencies:
-------------
- FastAPI and Pydantic
- Application service abstractions: RetrievalService, LLMService
- Dependency providers: get_embedding_provider, get_llm_provider, get_db
- Secure authentication (fastapi-users integration)

Security Considerations:
------------------------
- All endpoints are gated by robust, verified-user authentication.
- Only passive, minimal information is returned in the event of an error.

"""

from fastapi import APIRouter, Depends
from app.services.retrieval_service import RetrievalService
from app.services.llm_service import LLMService
from app.dependencies import get_llm_provider, get_embedding_provider
from app.db.core import get_db
from app.auth.router import fastapi_users

# Only allow active, verified users
current_active_user = fastapi_users.current_user(active=True, verified=True)

router = APIRouter(
    prefix="/rag",
    tags=["rag"],
    dependencies=[Depends(current_active_user)],
)


@router.post("/query")
async def query_rag(
    query: str,
    db=Depends(get_db),
    llm=Depends(get_llm_provider),
    emb=Depends(get_embedding_provider),
):
    """
    Retrieve relevant documents for a query and generate an answer using a language model.

    Args:
        query (str): The raw input query from the user.
        db: Database dependency for document retrieval.
        llm: The large language model provider dependency.
        emb: The embedding provider dependency.

    Returns:
        dict: A dictionary containing the generated answer as {"answer": answer}.
    """
    
    retriever = RetrievalService(db, emb)
    docs = await retriever.get_relevant_docs(query)
    answer = await LLMService(llm).generate_answer(query, docs)
    return {"answer": answer}
