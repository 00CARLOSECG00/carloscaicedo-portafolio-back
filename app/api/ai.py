"""AI assistant routes."""

from fastapi import APIRouter, HTTPException

from app.config import get_settings
from app.models.schemas import AIRequest, AIResponse, ErrorResponse
from app.services.ai_service import generate_chat_response

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post(
    "/chat",
    response_model=AIResponse,
    responses={400: {"model": ErrorResponse}},
)
async def chat(req: AIRequest) -> AIResponse:
    settings = get_settings()
    message = (req.message or "").strip()
    if not message:
        raise HTTPException(status_code=400, detail="Message is required.")
    if len(message) > settings.max_ai_message_length:
        raise HTTPException(status_code=400, detail="Message exceeds maximum length.")

    return await generate_chat_response(req, settings)
