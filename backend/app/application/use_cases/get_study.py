from uuid import UUID

from app.domain.models import Study
from app.domain.repositories import IStudyRepository


async def get_study(
    repo: IStudyRepository,
    study_id: UUID,
) -> Study | None:
    """Obtiene un estudio por su ID."""
    return await repo.get_by_id(study_id)