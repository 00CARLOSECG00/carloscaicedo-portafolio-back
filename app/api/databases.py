"""Database Lab routes."""

from fastapi import APIRouter, HTTPException

from app.models.schemas import (
    ColumnarResponse,
    DocumentResponse,
    ErrorResponse,
    GeospatialResponse,
    GraphResponse,
    KeyValueResponse,
    RelationalResponse,
    VectorSearchRequest,
    VectorSearchResponse,
)
from app.services import database_service

router = APIRouter(prefix="/databases", tags=["Databases"])


@router.get("/relational", response_model=RelationalResponse)
async def relational() -> RelationalResponse:
    return database_service.get_relational()


@router.get("/document", response_model=DocumentResponse)
async def document() -> DocumentResponse:
    return database_service.get_document()


@router.get("/columnar", response_model=ColumnarResponse)
async def columnar() -> ColumnarResponse:
    return database_service.get_columnar()


@router.get("/key-value", response_model=KeyValueResponse)
async def key_value() -> KeyValueResponse:
    return database_service.get_key_value()


@router.post(
    "/vector/search",
    response_model=VectorSearchResponse,
    responses={400: {"model": ErrorResponse}},
)
async def vector_search(req: VectorSearchRequest) -> VectorSearchResponse:
    query = (req.query or "").strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query is required.")
    top_k = req.top_k or 5
    return database_service.search_vectors(query, top_k=top_k)


@router.get("/graph", response_model=GraphResponse)
async def graph() -> GraphResponse:
    return database_service.get_graph()


@router.get("/geospatial", response_model=GeospatialResponse)
async def geospatial() -> GeospatialResponse:
    return database_service.get_geospatial()
