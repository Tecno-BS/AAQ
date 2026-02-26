import asyncio
from uuid import UUID
import logging 
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dto.schemas import AnalyzeAcceptedResponse
from app.application.use_cases.run_analysis_pipeline import run_analysis_pipeline
from app.infraestructure.repositories import ChartRepositoryImpl, StudyRepositoryImpl
from app.interfaces.api.deps import get_session

router = APIRouter(prefix="/studies", tags=["analysis"])

logger = logging.getLogger("aaq.analysis")

@router.post("/{study_id}/analyze", response_model=AnalyzeAcceptedResponse, status_code=202)
async def analyze_study_endpoint(
    study_id: UUID,
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

    # Usar create_task para que el pipeline corra independiente del request HTTP.
    # BackgroundTasks de FastAPI comparte el ciclo de vida del request y puede
    # ser cancelado cuando el cliente cierra la conexión (CancelledError).
    asyncio.get_event_loop().create_task(run_analysis_pipeline_sync(study_id))
    await study_repo.update_status(study_id, "analyzing")

    return AnalyzeAcceptedResponse(
        study_id=study_id,
        status="analyzing",
        message="Análisis iniciado. El reporte estará disponible cuando finalice.",
    )

async def run_analysis_pipeline_sync(study_id: UUID):
    from app.infraestructure.db.session import async_session_factory

    logger.info("[AAQ] Background task iniciado para study %s", study_id)
    try:
        async with async_session_factory() as session:
            try:
                await run_analysis_pipeline(session, study_id)
                logger.info("[AAQ] Pipeline OK, ejecutando commit para study %s", study_id)
                await session.commit()
                logger.info("[AAQ] COMMIT EXITOSO para study %s", study_id)
            except Exception as e:
                logger.exception("[AAQ] Error durante pipeline para study %s", study_id)
                await session.rollback()
                raise
    except Exception as e:
        logger.exception("[AAQ] Guardando failure_reason para study %s", study_id)
        try:
            async with async_session_factory() as err_session:
                from app.infraestructure.repositories import StudyRepositoryImpl
                repo = StudyRepositoryImpl(err_session)
                await repo.update_status(study_id, "failed", str(e))
                await err_session.commit()
        except Exception:
            logger.exception("[AAQ] No se pudo guardar failure_reason para study %s", study_id)
    finally:
        logger.info("[AAQ] Background task finalizado para study %s", study_id)