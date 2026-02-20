from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dto.schemas import (
    StudyCreateRequest,
    StudyDetailResponse,
    StudyResponse,
)
from app.application.use_cases import create_study, get_study
from app.infraestructure.repositories import ChartRepositoryImpl, StudyRepositoryImpl
from app.interfaces.api.deps import get_session

router = APIRouter(prefix="/studies", tags=["studies"])


@router.post("", response_model=StudyResponse, status_code=201)
async def create_study_endpoint(
    data: StudyCreateRequest,
    session: AsyncSession = Depends(get_session),
):
    """Crea un nuevo estudio con su contexto metodológico."""
    repo = StudyRepositoryImpl(session)
    study = await create_study(repo, data)
    return StudyResponse(
        id=study.id,
        status=study.status,
        created_at=study.created_at,
    )


@router.get("/{study_id}", response_model=StudyDetailResponse)
async def get_study_endpoint(
    study_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    """Obtiene el detalle de un estudio."""
    study_repo = StudyRepositoryImpl(session)
    chart_repo = ChartRepositoryImpl(session)
    
    study = await get_study(study_repo, study_id)
    if not study:
        raise HTTPException(status_code=404, detail="Study not found")
    
    charts_count = await chart_repo.count_by_study(study_id)
    
    return StudyDetailResponse(
        id=study.id,
        status=study.status,
        profile=study.context.profile,
        background=study.context.background,
        business_question=study.context.business_question,
        study_type=study.context.study_type,
        segments=study.context.segments,
        sample=study.context.sample,
        significance_threshold=study.context.significance_threshold,
        models=study.context.models,
        measurements=study.context.measurements,
        strategic_purposes=getattr(study.context, "strategic_purposes", []) or [],
        qualitative_study=study.context.qualitative_study,
        charts_count=charts_count,
        created_at=study.created_at,
        updated_at=study.updated_at,
        failure_reason=study.failure_reason,
    )