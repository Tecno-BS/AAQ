from uuid import UUID

from app.domain.repositories import IChartRepository, IStudyRepository
from app.application.use_cases.run_analysis_pipeline import run_analysis_pipeline


async def start_analysis(
    study_repo: IStudyRepository,
    chart_repo: IChartRepository,
    session,
    study_id: UUID,
) -> None:
    """
    Inicia el análisis de un estudio.
    """
    study = await study_repo.get_by_id(study_id)
    if not study:
        raise ValueError("Study not found")

    count = await chart_repo.count_by_study(study_id)
    if count == 0:
        raise ValueError("No charts uploaded. Upload at least one chart before analyzing.")

    await run_analysis_pipeline(session, study_id)