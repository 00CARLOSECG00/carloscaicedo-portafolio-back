"""Portfolio content routes — profile, projects, experience, education."""

from fastapi import APIRouter, HTTPException

from app.models.schemas import (
    AISuggestionsResponse,
    Education,
    Experience,
    MethodologyStep,
    Profile,
    ProfileContextChunk,
    Project,
)
from app.services import content_service

router = APIRouter(tags=["Content"])


@router.get("/profile", response_model=Profile)
async def profile() -> Profile:
    return content_service.get_profile()


@router.get("/projects", response_model=list[Project])
async def projects() -> list[Project]:
    return content_service.get_projects()


@router.get("/projects/{project_id}", response_model=Project)
async def project_by_id(project_id: str) -> Project:
    project = content_service.get_project_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project '{project_id}' not found.")
    return project


@router.get("/experience", response_model=list[Experience])
async def experience() -> list[Experience]:
    return content_service.get_experience()


@router.get("/education", response_model=list[Education])
async def education() -> list[Education]:
    return content_service.get_education()


@router.get("/methodology", response_model=list[MethodologyStep])
async def methodology() -> list[MethodologyStep]:
    return content_service.get_methodology()


@router.get("/profile-context", response_model=list[ProfileContextChunk])
async def profile_context() -> list[ProfileContextChunk]:
    return content_service.get_profile_context()


@router.get("/ai/suggestions", response_model=AISuggestionsResponse)
async def ai_suggestions() -> AISuggestionsResponse:
    return content_service.get_ai_suggestions()
