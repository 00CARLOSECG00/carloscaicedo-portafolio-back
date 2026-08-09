"""Knowledge graph routes."""

from fastapi import APIRouter, HTTPException

from app.models.schemas import ErrorResponse, KnowledgeGraphResponse, KnowledgeNode
from app.services import knowledge_service

router = APIRouter(prefix="/knowledge-graph", tags=["Knowledge Graph"])


@router.get("", response_model=KnowledgeGraphResponse)
async def get_graph() -> KnowledgeGraphResponse:
    return knowledge_service.get_knowledge_graph()


@router.get(
    "/nodes/{node_id}",
    response_model=KnowledgeNode,
    responses={404: {"model": ErrorResponse}},
)
async def get_node(node_id: str) -> KnowledgeNode:
    node = knowledge_service.get_knowledge_node(node_id)
    if not node:
        raise HTTPException(status_code=404, detail=f"Node '{node_id}' not found.")
    return node
