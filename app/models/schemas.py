"""Pydantic models matching the frontend TypeScript API contracts."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# AI Assistant
# ---------------------------------------------------------------------------

class AICardAction(BaseModel):
    label: str
    target: str


class AIContentCard(BaseModel):
    type: Literal["project", "database", "knowledge", "link"]
    id: str
    title: str
    description: str
    tags: list[str] | None = None
    action: AICardAction | None = None


class KnowledgeReference(BaseModel):
    type: Literal["knowledge", "project"]
    id: str
    label: str | None = None


class ChatHistoryMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class AIRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    message: str
    conversation_id: str | None = Field(default=None, alias="conversationId")
    history: list[ChatHistoryMessage] | None = None


class AIResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, serialize_by_alias=True)

    message: str
    cards: list[AIContentCard] | None = None
    references: list[KnowledgeReference] | None = None
    conversation_id: str | None = Field(default=None, alias="conversationId")


# ---------------------------------------------------------------------------
# NLP
# ---------------------------------------------------------------------------

class NLPRequest(BaseModel):
    text: str


class SentimentResponse(BaseModel):
    label: Literal["Positive", "Neutral", "Negative"]
    score: float


class EmotionScore(BaseModel):
    emotion: Literal["Joy", "Anger", "Sadness", "Fear", "Surprise"]
    score: float


class EmotionResponse(BaseModel):
    emotions: list[EmotionScore]


class LanguageResponse(BaseModel):
    language: str
    code: str
    confidence: float


class KeywordsResponse(BaseModel):
    keywords: list[str]


class Entity(BaseModel):
    text: str
    type: Literal["PERSON", "ORG", "LOCATION", "DATE"]
    start: int
    end: int


class EntitiesResponse(BaseModel):
    entities: list[Entity]


class SummarizeResponse(BaseModel):
    summary: str


# ---------------------------------------------------------------------------
# Databases
# ---------------------------------------------------------------------------

class RelationalTable(BaseModel):
    name: str
    columns: list[str]
    rows: list[list[str | int | float]]


class RelationalResponse(BaseModel):
    tables: list[RelationalTable]


class DocumentResponse(BaseModel):
    collection: str
    documents: list[dict]


class ColumnarColumn(BaseModel):
    name: str
    type: str
    values: list[str | int | float]
    note: str


class ColumnarResponse(BaseModel):
    table: str
    columns: list[ColumnarColumn]


class KeyValueEntry(BaseModel):
    key: str
    value: dict


class KeyValueResponse(BaseModel):
    entries: list[KeyValueEntry]


class VectorRecord(BaseModel):
    id: str
    label: str
    description: str
    x: float
    y: float
    score: float | None = None


class VectorSearchRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    query: str
    top_k: int | None = Field(default=5, alias="topK")


class VectorSearchResponse(BaseModel):
    query: str
    records: list[VectorRecord]


class GraphNode(BaseModel):
    id: str
    label: str
    group: str | None = None


class GraphEdge(BaseModel):
    source: str
    target: str
    label: str | None = None


class GraphResponse(BaseModel):
    nodes: list[GraphNode]
    edges: list[GraphEdge]


class GeoFeature(BaseModel):
    id: str
    label: str
    latitude: float
    longitude: float
    value: int | float | None = None
    category: str | None = None


class GeospatialResponse(BaseModel):
    features: list[GeoFeature]


# ---------------------------------------------------------------------------
# Knowledge Graph
# ---------------------------------------------------------------------------

class KnowledgeNode(BaseModel):
    id: str
    label: str
    group: str
    description: str
    related: list[str]
    projects: list[str] | None = None
    technologies: list[str] | None = None


class KnowledgeGraphResponse(BaseModel):
    nodes: list[KnowledgeNode]
    edges: list[GraphEdge]


class ErrorResponse(BaseModel):
    error: str


# ---------------------------------------------------------------------------
# Profile & Portfolio Content (Supabase-driven)
# ---------------------------------------------------------------------------

class ProfileLinks(BaseModel):
    linkedin: str
    github: str
    email: str
    resume: str


class Profile(BaseModel):
    name: str
    title: str
    tagline: str
    description: str
    bio: str | None = None
    links: ProfileLinks
    linkedin_handle: str | None = None
    github_handle: str | None = None


class Project(BaseModel):
    id: str
    title: str
    description: str
    category: str
    accent: str = "primary"
    technologies: list[str] | None = None
    target: str | None = None
    url: str | None = None


class Experience(BaseModel):
    id: str
    company: str
    role: str
    description: str
    start_date: str | None = None
    end_date: str | None = None
    is_current: bool = False
    technologies: list[str] | None = None


class Education(BaseModel):
    id: str
    institution: str
    degree: str
    field: str | None = None
    description: str | None = None
    start_date: str | None = None
    end_date: str | None = None


class MethodologyStep(BaseModel):
    label: str
    detail: str
    sort_order: int = 0


class ProfileContextChunk(BaseModel):
    category: str
    title: str | None = None
    content: str


class AISuggestionsResponse(BaseModel):
    suggestions: list[str]
