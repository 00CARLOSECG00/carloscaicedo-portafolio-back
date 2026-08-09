"""NLP playground routes — each tool fails independently."""

from fastapi import APIRouter, HTTPException

from app.config import get_settings
from app.models.schemas import (
    EmotionResponse,
    EntitiesResponse,
    ErrorResponse,
    KeywordsResponse,
    LanguageResponse,
    NLPRequest,
    SentimentResponse,
    SummarizeResponse,
)
from app.services import nlp_service

router = APIRouter(prefix="/nlp", tags=["NLP"])


def _validate_text(text: str) -> str:
    settings = get_settings()
    cleaned = (text or "").strip()
    if not cleaned:
        raise HTTPException(status_code=400, detail="Text is required.")
    if len(cleaned) > settings.max_nlp_input_length:
        raise HTTPException(status_code=400, detail="Text exceeds maximum length.")
    return cleaned


@router.post("/sentiment", response_model=SentimentResponse, responses={400: {"model": ErrorResponse}})
async def sentiment(req: NLPRequest) -> SentimentResponse:
    return nlp_service.analyze_sentiment(_validate_text(req.text))


@router.post("/emotion", response_model=EmotionResponse, responses={400: {"model": ErrorResponse}})
async def emotion(req: NLPRequest) -> EmotionResponse:
    return nlp_service.analyze_emotion(_validate_text(req.text))


@router.post("/language", response_model=LanguageResponse, responses={400: {"model": ErrorResponse}})
async def language(req: NLPRequest) -> LanguageResponse:
    return nlp_service.detect_language(_validate_text(req.text))


@router.post("/keywords", response_model=KeywordsResponse, responses={400: {"model": ErrorResponse}})
async def keywords(req: NLPRequest) -> KeywordsResponse:
    return nlp_service.extract_keywords(_validate_text(req.text))


@router.post("/entities", response_model=EntitiesResponse, responses={400: {"model": ErrorResponse}})
async def entities(req: NLPRequest) -> EntitiesResponse:
    return nlp_service.extract_entities(_validate_text(req.text))


@router.post("/summarize", response_model=SummarizeResponse, responses={400: {"model": ErrorResponse}})
async def summarize(req: NLPRequest) -> SummarizeResponse:
    return nlp_service.summarize_text(_validate_text(req.text))
