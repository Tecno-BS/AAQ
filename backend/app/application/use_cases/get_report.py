from uuid import UUID

from app.domain.models import ExecutiveReport
from app.domain.repositories import IReportRepository


async def get_report(
    repo: IReportRepository,
    study_id: UUID,
) -> ExecutiveReport | None:
    """Obtiene el reporte de un estudio."""
    return await repo.get_by_study(study_id)