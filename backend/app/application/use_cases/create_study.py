from datetime import datetime
from uuid import uuid4

from app.application.dto.schemas import StudyCreateRequest
from app.domain.models import ResearchContext, Study
from app.domain.repositories import IStudyRepository


async def create_study(
    repo: IStudyRepository,
    data: StudyCreateRequest,
) -> Study:
    """Crea un nuevo estudio con su contexto metodológico."""
    
    context = ResearchContext(
        profile=data.profile,
        background=data.background,
        business_question=data.business_question,
        study_type=data.study_type,
        segments=data.segments,
        sample=data.sample,
        significance_threshold=data.significance_threshold,
        models=data.models,
        measurements=data.measurements,
        strategic_purposes=getattr(data, "strategic_purposes", []) or [],
        qualitative_study=data.qualitative_study,
    )
    
    now = datetime.utcnow()
    study = Study(
        id=uuid4(),
        context=context,
        status="draft",
        created_at=now,
        updated_at=now,
    )
    
    return await repo.create(study)