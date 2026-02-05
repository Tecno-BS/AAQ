from datetime import datetime
from uuid import UUID, uuid4

from app.domain.models import Chart
from app.domain.repositories import IChartRepository, IStudyRepository


async def upload_charts(
    study_repo: IStudyRepository,
    chart_repo: IChartRepository,
    study_id: UUID,
    files_data: list[dict],  # [{"filename": str, "storage_path": str, "mime_type": str}]
) -> list[Chart]:
    """
    Registra las gráficas subidas para un estudio.
    
    Args:
        study_repo: Repositorio de estudios
        chart_repo: Repositorio de gráficas
        study_id: ID del estudio
        files_data: Lista de diccionarios con filename, storage_path y mime_type
    
    Returns:
        Lista de Chart creados
    """
    # Verificar que el estudio existe
    study = await study_repo.get_by_id(study_id)
    if not study:
        raise ValueError("Study not found")
    
    # Verificar estado válido para subir gráficas
    if study.status not in ("draft", "charts_uploaded"):
        raise ValueError(f"Cannot upload charts when study is in '{study.status}' status")
    
    charts = []
    now = datetime.utcnow()
    
    for file_data in files_data:
        chart = Chart(
            id=uuid4(),
            study_id=study_id,
            original_filename=file_data["filename"],
            storage_path=file_data["storage_path"],
            mime_type=file_data["mime_type"],
            created_at=now,
        )
        created_chart = await chart_repo.create(chart)
        charts.append(created_chart)
    
    # Actualizar estado del estudio
    await study_repo.update_status(study_id, "charts_uploaded")
    
    return charts
