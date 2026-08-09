"""Portfolio content from Supabase with static fallbacks."""

from __future__ import annotations

import logging

from app.config import Settings, get_settings
from app.data.fallback_content import (
    FALLBACK_AI_SUGGESTIONS,
    FALLBACK_EDUCATION,
    FALLBACK_EXPERIENCE,
    FALLBACK_METHODOLOGY,
    FALLBACK_PROFILE,
    FALLBACK_PROFILE_CONTEXT,
    FALLBACK_PROJECTS,
)
from app.models.schemas import (
    AISuggestionsResponse,
    Education,
    Experience,
    MethodologyStep,
    Profile,
    ProfileContextChunk,
    Project,
)
from app.services.supabase_client import get_supabase_client

logger = logging.getLogger(__name__)


def get_profile(settings: Settings | None = None) -> Profile:
    settings = settings or get_settings()
    client = get_supabase_client(settings)
    if client and settings.use_supabase_content:
        try:
            resp = client.table("site_profile").select("*").eq("id", "default").maybe_single().execute()
            if resp.data:
                row = resp.data
                from app.models.schemas import ProfileLinks

                return Profile(
                    name=row["name"],
                    title=row["title"],
                    tagline=row["tagline"],
                    description=row["description"],
                    bio=row.get("bio"),
                    links=ProfileLinks(
                        linkedin=row["linkedin_url"],
                        github=row["github_url"],
                        email=row["email"],
                        resume=row.get("resume_url") or "/resume.pdf",
                    ),
                    linkedin_handle=row.get("linkedin_handle"),
                    github_handle=row.get("github_handle"),
                )
        except Exception as exc:
            logger.warning("Supabase profile fetch failed: %s", exc)
    return FALLBACK_PROFILE


def get_projects(settings: Settings | None = None) -> list[Project]:
    settings = settings or get_settings()
    client = get_supabase_client(settings)
    if client and settings.use_supabase_content:
        try:
            resp = (
                client.table("projects")
                .select("*")
                .eq("is_active", True)
                .order("sort_order")
                .execute()
            )
            if resp.data:
                return [
                    Project(
                        id=row["id"],
                        title=row["title"],
                        description=row["description"],
                        category=row["category"],
                        accent=row.get("accent") or "primary",
                        technologies=row.get("technologies"),
                        target=row.get("target"),
                        url=row.get("url"),
                    )
                    for row in resp.data
                ]
        except Exception as exc:
            logger.warning("Supabase projects fetch failed: %s", exc)
    return FALLBACK_PROJECTS


def get_project_by_id(project_id: str, settings: Settings | None = None) -> Project | None:
    return next((p for p in get_projects(settings) if p.id == project_id), None)


def get_experience(settings: Settings | None = None) -> list[Experience]:
    settings = settings or get_settings()
    client = get_supabase_client(settings)
    if client and settings.use_supabase_content:
        try:
            resp = (
                client.table("experience")
                .select("*")
                .eq("is_active", True)
                .order("sort_order")
                .execute()
            )
            if resp.data:
                return [
                    Experience(
                        id=str(row["id"]),
                        company=row["company"],
                        role=row["role"],
                        description=row["description"],
                        start_date=row.get("start_date"),
                        end_date=row.get("end_date"),
                        is_current=row.get("is_current", False),
                        technologies=row.get("technologies"),
                    )
                    for row in resp.data
                ]
        except Exception as exc:
            logger.warning("Supabase experience fetch failed: %s", exc)
    return FALLBACK_EXPERIENCE


def get_education(settings: Settings | None = None) -> list[Education]:
    settings = settings or get_settings()
    client = get_supabase_client(settings)
    if client and settings.use_supabase_content:
        try:
            resp = (
                client.table("education")
                .select("*")
                .eq("is_active", True)
                .order("sort_order")
                .execute()
            )
            if resp.data:
                return [
                    Education(
                        id=str(row["id"]),
                        institution=row["institution"],
                        degree=row["degree"],
                        field=row.get("field"),
                        description=row.get("description"),
                        start_date=row.get("start_date"),
                        end_date=row.get("end_date"),
                    )
                    for row in resp.data
                ]
        except Exception as exc:
            logger.warning("Supabase education fetch failed: %s", exc)
    return FALLBACK_EDUCATION


def get_methodology(settings: Settings | None = None) -> list[MethodologyStep]:
    settings = settings or get_settings()
    client = get_supabase_client(settings)
    if client and settings.use_supabase_content:
        try:
            resp = (
                client.table("methodology_steps")
                .select("*")
                .eq("is_active", True)
                .order("sort_order")
                .execute()
            )
            if resp.data:
                return [
                    MethodologyStep(label=row["label"], detail=row["detail"], sort_order=row["sort_order"])
                    for row in resp.data
                ]
        except Exception as exc:
            logger.warning("Supabase methodology fetch failed: %s", exc)
    return FALLBACK_METHODOLOGY


def get_ai_suggestions(settings: Settings | None = None) -> AISuggestionsResponse:
    settings = settings or get_settings()
    client = get_supabase_client(settings)
    if client and settings.use_supabase_content:
        try:
            resp = (
                client.table("ai_suggestions")
                .select("text")
                .eq("is_active", True)
                .order("sort_order")
                .execute()
            )
            if resp.data:
                return AISuggestionsResponse(suggestions=[row["text"] for row in resp.data])
        except Exception as exc:
            logger.warning("Supabase AI suggestions fetch failed: %s", exc)
    return AISuggestionsResponse(suggestions=FALLBACK_AI_SUGGESTIONS)


def get_profile_context(settings: Settings | None = None) -> list[ProfileContextChunk]:
    settings = settings or get_settings()
    client = get_supabase_client(settings)
    if client and settings.use_supabase_content:
        try:
            resp = (
                client.table("profile_context")
                .select("*")
                .eq("is_active", True)
                .order("sort_order")
                .execute()
            )
            if resp.data:
                return [
                    ProfileContextChunk(
                        category=row["category"],
                        title=row.get("title"),
                        content=row["content"],
                    )
                    for row in resp.data
                ]
        except Exception as exc:
            logger.warning("Supabase profile context fetch failed: %s", exc)
    return FALLBACK_PROFILE_CONTEXT


def build_ai_context_block(settings: Settings | None = None) -> str:
    """Assemble all profile data into a text block for the Groq system prompt."""
    settings = settings or get_settings()
    profile = get_profile(settings)
    projects = get_projects(settings)
    experience = get_experience(settings)
    education = get_education(settings)
    chunks = get_profile_context(settings)

    lines = [
        f"Name: {profile.name}",
        f"Title: {profile.title}",
        f"Tagline: {profile.tagline}",
    ]
    if profile.bio:
        lines.append(f"Bio: {profile.bio}")

    if chunks:
        lines.append("\nAdditional context:")
        for c in chunks:
            header = f"{c.title}: " if c.title else ""
            lines.append(f"- [{c.category}] {header}{c.content}")

    if experience:
        lines.append("\nWork experience:")
        for e in experience:
            period = f"{e.start_date or '?'} – {e.end_date or 'Present' if e.is_current else e.end_date or '?'}"
            tech = f" Technologies: {', '.join(e.technologies)}." if e.technologies else ""
            lines.append(f"- {e.role} at {e.company} ({period}). {e.description}{tech}")

    if education:
        lines.append("\nEducation:")
        for ed in education:
            field = f" in {ed.field}" if ed.field else ""
            period = f" ({ed.start_date or ''}–{ed.end_date or ''})" if ed.start_date or ed.end_date else ""
            desc = f" {ed.description}" if ed.description else ""
            lines.append(f"- {ed.degree}{field} — {ed.institution}{period}.{desc}")

    if projects:
        lines.append("\nActive projects:")
        for p in projects:
            tech = f" [{', '.join(p.technologies)}]" if p.technologies else ""
            lines.append(f"- {p.id}: {p.title} — {p.description}{tech}")

    return "\n".join(lines)
