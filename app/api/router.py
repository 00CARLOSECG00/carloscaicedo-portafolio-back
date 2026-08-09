"""Aggregate API router."""

from fastapi import APIRouter

from app.api import ai, content, databases, knowledge, nlp

api_router = APIRouter()
api_router.include_router(ai.router)
api_router.include_router(nlp.router)
api_router.include_router(databases.router)
api_router.include_router(knowledge.router)
api_router.include_router(content.router)
