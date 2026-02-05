from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models import ResearchContext, Study
from app.domain.repositories import IStudyRepository
from app.infraestructure.db.models import ResearchContextORM, StudyORM


def _orm_to_study(study_orm: StudyORM, context_orm: ResearchContextORM) -> Study:
    ctx = ResearchContext(
        profile=context_orm.profile,
        background=context_orm.background,
        business_question=context_orm.business_question,
        study_type=context_orm.study_type,
        segments=context_orm.segments or [],
        sample=context_orm.sample,
        significance_threshold=context_orm.significance_threshold,
        models=context_orm.models or [],
        measurements=context_orm.measurements or [],
        qualitative_study=context_orm.qualitative_study,
    )
    return Study(
        id=study_orm.id,
        context=ctx,
        status=study_orm.status,
        created_at=study_orm.created_at,
        updated_at=study_orm.updated_at,
        failure_reason=study_orm.failure_reason,
    )


class StudyRepositoryImpl(IStudyRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, study: Study) -> Study:
        study_id = study.id if study.id else uuid4()
        now = datetime.utcnow()

        study_orm = StudyORM(
            id=study_id,
            status=study.status,
            failure_reason=study.failure_reason,
            created_at=now,
            updated_at=now,
        )

        ctx = study.context
        ctx_orm = ResearchContextORM(
            study_id=study_id,
            profile=ctx.profile,
            background=ctx.background,
            business_question=ctx.business_question,
            study_type=ctx.study_type,
            segments=ctx.segments,
            sample=ctx.sample,
            significance_threshold=ctx.significance_threshold,
            models=ctx.models,
            measurements=ctx.measurements,
            qualitative_study=ctx.qualitative_study,
        )

        self._session.add(study_orm)
        self._session.add(ctx_orm)
        await self._session.flush()

        return Study(
            id=study_orm.id,
            context=study.context,
            status=study_orm.status,
            created_at=study_orm.created_at,
            updated_at=study_orm.updated_at,
            failure_reason=study_orm.failure_reason,
        )

    async def get_by_id(self, study_id: UUID) -> Study | None:
        result = await self._session.execute(
            select(StudyORM, ResearchContextORM)
            .join(ResearchContextORM, ResearchContextORM.study_id == StudyORM.id)
            .where(StudyORM.id == study_id)
        )
        row = result.first()
        if not row:
            return None
        study_orm, ctx_orm = row
        return _orm_to_study(study_orm, ctx_orm)

    async def update(self, study: Study) -> Study:
        result = await self._session.execute(
            select(StudyORM).where(StudyORM.id == study.id)
        )
        study_orm = result.scalar_one_or_none()
        if not study_orm:
            raise ValueError(f"Study {study.id} not found")

        study_orm.status = study.status
        study_orm.failure_reason = study.failure_reason
        study_orm.updated_at = datetime.utcnow()

        ctx = study.context
        ctx_result = await self._session.execute(
            select(ResearchContextORM).where(ResearchContextORM.study_id == study.id)
        )
        ctx_orm = ctx_result.scalar_one_or_none()
        if ctx_orm:
            ctx_orm.profile = ctx.profile
            ctx_orm.background = ctx.background
            ctx_orm.business_question = ctx.business_question
            ctx_orm.study_type = ctx.study_type
            ctx_orm.segments = ctx.segments
            ctx_orm.sample = ctx.sample
            ctx_orm.significance_threshold = ctx.significance_threshold
            ctx_orm.models = ctx.models
            ctx_orm.measurements = ctx.measurements
            ctx_orm.qualitative_study = ctx.qualitative_study

        await self._session.flush()
        return study

    async def update_status(
        self, study_id: UUID, status: str, failure_reason: str | None = None
    ) -> None:
        result = await self._session.execute(
            select(StudyORM).where(StudyORM.id == study_id)
        )
        study_orm = result.scalar_one_or_none()
        if not study_orm:
            raise ValueError(f"Study {study_id} not found")

        study_orm.status = status
        study_orm.failure_reason = failure_reason
        study_orm.updated_at = datetime.utcnow()
        await self._session.flush()

    async def list(self, limit: int = 50, offset: int = 0) -> list[Study]:
        result = await self._session.execute(
            select(StudyORM, ResearchContextORM)
            .join(ResearchContextORM, ResearchContextORM.study_id == StudyORM.id)
            .order_by(StudyORM.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return [_orm_to_study(s, c) for s, c in result.all()]