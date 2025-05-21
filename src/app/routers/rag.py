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
