from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.auth.admin import router as admin_router
from app.auth.router import router as auth_router, fastapi_users
from app.schemas import UserRead, UserUpdate
from app.routers.rag import router as rag_router
from app.routers.agent import router as agent_router
from app.routers.tavily import router as tavily_router

# Dependencies to protect endpoints
current_active = fastapi_users.current_user(active=True)
current_verified = fastapi_users.current_user(active=True, verified=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)

app = FastAPI(title="Your App with Auth + RAG")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication and admin routes
app.include_router(auth_router)
app.include_router(admin_router)

# User management routes (only superusers)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(current_superuser)],
)

# Public RAG endpoints
app.include_router(rag_router)

# Protected Tavily endpoints (requires active user)
app.include_router(
    tavily_router,
    dependencies=[Depends(current_verified)],
)

# Protected Agent endpoints (requires active + verified user)
app.include_router(
    agent_router,
    dependencies=[Depends(current_verified)],
)

@app.get("/")
async def health_check():
    return {"status": "ok"}