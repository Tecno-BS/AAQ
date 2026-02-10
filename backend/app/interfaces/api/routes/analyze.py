from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dto.schemas import AnalyzeAcceptedResponse
from app.application.use_cases.run_analysis_pipeline import run_analysis_pipeline
from app.infraestructure.repositories import ChartRepositoryImpl, StudyRepositoryImpl
from app.interfaces.api.deps import get_session

router = APIRouter(prefix="/studies", tags=["analysis"])


@router.post("/{study_id}/analyze", response_model=AnalyzeAcceptedResponse, status_code=202)
async def analyze_study_endpoint(
    study_id: UUID,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
):
    """
    Inicia el análisis de un estudio.
    """
    study_repo = StudyRepositoryImpl(session)
    chart_repo = ChartRepositoryImpl(session)

    study = await study_repo.get_by_id(study_id)
    if not study:
        raise HTTPException(status_code=404, detail="Study not found")

    count = await chart_repo.count_by_study(study_id)
    if count == 0:
        raise HTTPException(
            status_code=400,
            detail="No charts uploaded. Upload at least one chart before analyzing.",
        )

    background_tasks.add_task(run_analysis_pipeline_sync, study_id)
    await study_repo.update_status(study_id, "analyzing")

    return AnalyzeAcceptedResponse(
        study_id=study_id,
        status="analyzing",
        message="Análisis iniciado. El reporte estará disponible cuando finalice.",
    )

async def run_analysis_pipeline_sync(study_id: UUID):
    #Wrapper para ejecutar el pipeline en background con su propia sesión
    from app.application.use_cases.run_analysis_pipeline import async_session_factory

    async with async_session_factory() as session:
        try:
            await run_analysis_pipeline(session, study_id)
        except Exception:
            from app.infraestructure.repositories import StudyRepositoryImpl
            repo = StudyRepositoryImpl(session)
            await repo.update_status(study_id, "failed", "Error al ejecutar el análisis")