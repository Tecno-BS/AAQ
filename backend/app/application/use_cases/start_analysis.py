from uuid import UUID

from app.domain.repositories import IChartRepository, IStudyRepository


async def start_analysis(
    study_repo: IStudyRepository,
    chart_repo: IChartRepository,
    study_id: UUID,
) -> None:
    """
    Inicia el análisis de un estudio.
    
    Por ahora solo cambia el estado a 'analyzing'.
    En la Fase 2.2 se conectará con el pipeline LangGraph.
    """
    # Verificar que el estudio existe
    study = await study_repo.get_by_id(study_id)
    if not study:
        raise ValueError("Study not found")
    
    # Verificar que hay gráficas
    charts_count = await chart_repo.count_by_study(study_id)
    if charts_count == 0:
        raise ValueError("No charts uploaded")
    
    # Verificar estado válido
    if study.status not in ("charts_uploaded",):
        raise ValueError(f"Cannot start analysis when study is in '{study.status}' status")
    
    # Cambiar estado a analyzing
    await study_repo.update_status(study_id, "analyzing")
    
    # TODO: En Fase 2.2, aquí se encolará el job del pipeline LangGraph