from fastapi import FastAPI
from .routers import auth, users, rag

app = FastAPI(title="RAG + Auth API")
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(rag.router)
