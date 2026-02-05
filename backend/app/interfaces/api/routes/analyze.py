from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dto.schemas import AnalyzeAcceptedResponse
from app.application.use_cases import start_analysis
from app.infraestructure.repositories import ChartRepositoryImpl, StudyRepositoryImpl
from app.interfaces.api.deps import get_session

router = APIRouter(prefix="/studies", tags=["analysis"])


@router.post("/{study_id}/analyze", response_model=AnalyzeAcceptedResponse, status_code=202)
async def analyze_study_endpoint(
    study_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    """
    Inicia el análisis de un estudio.
    
    Por ahora solo cambia el estado a 'analyzing'.
    El pipeline cognitivo se implementará en la Fase 2.2.
    """
    study_repo = StudyRepositoryImpl(session)
    chart_repo = ChartRepositoryImpl(session)
    
    try:
        await start_analysis(study_repo, chart_repo, study_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return AnalyzeAcceptedResponse(
        study_id=study_id,
        status="analyzing",
        message="Análisis iniciado correctamente.",
    )