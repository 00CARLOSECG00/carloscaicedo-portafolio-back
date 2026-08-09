"""AI assistant — Groq LLM with dynamic context from Supabase."""

from __future__ import annotations

import json
import logging
import re
from typing import Any

from app.config import Settings, get_settings
from app.models.schemas import AIContentCard, AICardAction, AIRequest, AIResponse, KnowledgeReference, Project
from app.services.content_service import (
    build_ai_context_block,
    get_ai_suggestions,
    get_projects,
)

logger = logging.getLogger(__name__)

JSON_SCHEMA_INSTRUCTIONS = """
You MUST respond with valid JSON only (no markdown fences), matching this schema:
{
  "message": "natural language answer string",
  "cards": [
    {
      "type": "project" | "database" | "knowledge" | "link",
      "id": "string",
      "title": "string",
      "description": "string",
      "tags": ["optional"],
      "action": { "label": "string", "target": "#section-anchor" }
    }
  ],
  "references": [
    { "type": "knowledge" | "project", "id": "string", "label": "optional string" }
  ]
}

Include relevant cards when the user asks about projects, experience, education, databases, NLP, RAG, or skills.
Keep answers helpful for recruiters and technical visitors.
ONLY use facts from the profile context below — do not invent employers, degrees, or projects.
Section anchors: #ai, #nlp, #databases, #knowledge, #projects, #experience, #contact
"""


def _build_system_prompt(settings: Settings) -> str:
    context = build_ai_context_block(settings)
    projects = get_projects(settings)
    project_ids = ", ".join(p.id for p in projects) or "none"
    return (
        f"You are the AI assistant on the portfolio website of the person described below.\n"
        f"Answer questions professionally and concisely in English.\n\n"
        f"=== PROFILE DATA (source of truth) ===\n{context}\n\n"
        f"Available project ids for cards: {project_ids}\n"
        f"Knowledge graph ids: ai, ml, nlp, llms, rag, embeddings, vector-db, databases, "
        f"relational, document, columnar, key-value, graph, geospatial\n"
        f"{JSON_SCHEMA_INSTRUCTIONS}"
    )


def _project_card(project: Project) -> AIContentCard:
    return AIContentCard(
        type="project",
        id=project.id,
        title=project.title,
        description=project.description,
        tags=project.technologies,
        action=AICardAction(label="Explore project", target=project.target or "#projects"),
    )


def _fallback_response(message: str, settings: Settings) -> AIResponse:
    """Simple keyword fallback using live project list from Supabase/static."""
    q = message.lower()
    projects = get_projects(settings)

    if any(t in q for t in ("project", "built", "build", "portfolio", "work")):
        return AIResponse(
            message="Here are the interactive projects you can explore right now.",
            cards=[_project_card(p) for p in projects],
        )

    if any(t in q for t in ("experience", "job", "worked", "career", "employer")):
        return AIResponse(
            message="You can find work experience details in the Experience section, or ask me about specific roles.",
            cards=[AIContentCard(
                type="link", id="experience", title="Experience",
                description="Work history and roles.",
                action=AICardAction(label="View experience", target="#experience"),
            )],
        )

    if any(t in q for t in ("education", "study", "university", "degree", "school")):
        return AIResponse(
            message="Education details are available in the Education section below.",
            cards=[AIContentCard(
                type="link", id="education", title="Education",
                description="Degrees and academic background.",
                action=AICardAction(label="View education", target="#education"),
            )],
        )

    if any(t in q for t in ("contact", "email", "hire", "reach", "linkedin", "github", "resume")):
        return AIResponse(
            message="You can reach out via LinkedIn, GitHub or email in the Let's Connect section.",
            cards=[AIContentCard(
                type="link", id="contact", title="Let's Connect",
                description="LinkedIn, GitHub, email and resume.",
                action=AICardAction(label="Go to contact", target="#contact"),
            )],
        )

    suggestions = get_ai_suggestions(settings).suggestions[:3]
    hint = " Try asking: " + "; ".join(suggestions) if suggestions else ""
    return AIResponse(
        message=f"I can tell you about specialties, projects, experience, education, and technical skills.{hint}",
        cards=[_project_card(p) for p in projects[:2]],
        references=[KnowledgeReference(type="knowledge", id="ai", label="AI")],
    )


def _parse_llm_json(content: str) -> dict[str, Any] | None:
    content = content.strip()
    if content.startswith("```"):
        content = re.sub(r"^```(?:json)?\s*", "", content)
        content = re.sub(r"\s*```$", "", content)
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                return None
    return None


async def _groq_chat(req: AIRequest, settings: Settings) -> AIResponse | None:
    try:
        from groq import AsyncGroq

        client = AsyncGroq(api_key=settings.groq_api_key)
        system_prompt = _build_system_prompt(settings)
        messages: list[dict[str, str]] = [{"role": "system", "content": system_prompt}]
        if req.history:
            for msg in req.history[-10:]:
                messages.append({"role": msg.role, "content": msg.content})
        messages.append({"role": "user", "content": req.message})

        completion = await client.chat.completions.create(
            model=settings.groq_model,
            messages=messages,
            temperature=0.4,
            max_tokens=1024,
            response_format={"type": "json_object"},
        )
        raw = completion.choices[0].message.content or ""
        parsed = _parse_llm_json(raw)
        if not parsed or "message" not in parsed:
            return None

        return AIResponse(
            message=parsed["message"],
            cards=parsed.get("cards"),
            references=parsed.get("references"),
            conversation_id=req.conversation_id,
        )
    except Exception as exc:
        logger.warning("Groq chat failed, using fallback: %s", exc)
        return None


async def generate_chat_response(req: AIRequest, settings: Settings | None = None) -> AIResponse:
    settings = settings or get_settings()
    if settings.groq_enabled:
        groq_response = await _groq_chat(req, settings)
        if groq_response:
            return groq_response

    response = _fallback_response(req.message, settings)
    response.conversation_id = req.conversation_id
    return response
