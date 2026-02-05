from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models import ChartAnalysis
from app.domain.repositories import IAnalysisRepository
from app.infraestructure.db.models import AnalysisORM


def _orm_to_analysis(analysis_orm: AnalysisORM) -> ChartAnalysis:
    return ChartAnalysis(
        id=analysis_orm.id,
        chart_id=analysis_orm.chart_id,
        study_id=analysis_orm.study_id,
        explanation=analysis_orm.explanation,
        hypotheses=analysis_orm.hypotheses or [],
        business_impact=analysis_orm.business_impact,
        created_at=analysis_orm.created_at,
    )


class AnalysisRepositoryImpl(IAnalysisRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, analysis: ChartAnalysis) -> ChartAnalysis:
        analysis_id = analysis.id if analysis.id else uuid4()
        now = datetime.utcnow()

        analysis_orm = AnalysisORM(
            id=analysis_id,
            chart_id=analysis.chart_id,
            study_id=analysis.study_id,
            explanation=analysis.explanation,
            hypotheses=analysis.hypotheses,
            business_impact=analysis.business_impact,
            created_at=now,
        )

        self._session.add(analysis_orm)
        await self._session.flush()

        return ChartAnalysis(
            id=analysis_orm.id,
            chart_id=analysis_orm.chart_id,
            study_id=analysis_orm.study_id,
            explanation=analysis_orm.explanation,
            hypotheses=analysis_orm.hypotheses or [],
            business_impact=analysis_orm.business_impact,
            created_at=analysis_orm.created_at,
        )

    async def get_by_id(self, analysis_id: UUID) -> ChartAnalysis | None:
        result = await self._session.execute(
            select(AnalysisORM).where(AnalysisORM.id == analysis_id)
        )
        analysis_orm = result.scalar_one_or_none()
        if not analysis_orm:
            return None
        return _orm_to_analysis(analysis_orm)

    async def get_by_chart(self, chart_id: UUID) -> ChartAnalysis | None:
        result = await self._session.execute(
            select(AnalysisORM).where(AnalysisORM.chart_id == chart_id)
        )
        analysis_orm = result.scalar_one_or_none()
        if not analysis_orm:
            return None
        return _orm_to_analysis(analysis_orm)

    async def list_by_study(
        self, study_id: UUID, limit: int = 100, offset: int = 0
    ) -> list[ChartAnalysis]:
        result = await self._session.execute(
            select(AnalysisORM)
            .where(AnalysisORM.study_id == study_id)
            .order_by(AnalysisORM.created_at.asc())
            .limit(limit)
            .offset(offset)
        )
        return [_orm_to_analysis(a) for a in result.scalars().all()]