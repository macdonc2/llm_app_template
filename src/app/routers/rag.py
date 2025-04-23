from fastapi import APIRouter, Depends
from ..services.retrieval_service import RetrievalService
from ..services.llm_service import LLMService
from ..dependencies import get_llm_provider, get_embedding_provider
from ..db import get_db

router = APIRouter(prefix="/rag", tags=["rag"])

@router.post("/query")
async def query_rag(query: str, db=Depends(get_db),
                    llm=Depends(get_llm_provider),
                    emb=Depends(get_embedding_provider)):
    retriever = RetrievalService(db, emb)
    docs = await retriever.get_relevant_docs(query)
    answer = await LLMService(llm).generate_answer(query, docs)
    return {"answer": answer}
