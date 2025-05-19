from fastapi import FastAPI
from .routers import auth, users, rag, tavily, agent
from app.routers.tavily import router as tavily_router

app = FastAPI(title="RAG + Auth API")
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(rag.router)
app.include_router(tavily.router)
app.include_router(agent.router)


@app.get("/")
def root():
    return {"status": "ok"}
