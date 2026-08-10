"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.config import get_settings

settings = get_settings()

app = FastAPI(
    title="Carlos Caicedo Portfolio API",
    description="Backend for the AI & Data portfolio — AI chat, NLP, Database Lab, Knowledge Graph.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.api_prefix)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "environment": settings.environment}


@app.get("/")
async def root() -> dict[str, str]:
    return {
        "name": "Carlos Caicedo Portfolio API",
        "docs": "/docs",
        "health": "/health",
    }
