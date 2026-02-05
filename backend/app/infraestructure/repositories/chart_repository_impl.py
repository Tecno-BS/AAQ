from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models import Chart
from app.domain.repositories import IChartRepository
from app.infraestructure.db.models import ChartORM


def _orm_to_chart(chart_orm: ChartORM) -> Chart:
    return Chart(
        id=chart_orm.id,
        study_id=chart_orm.study_id,
        original_filename=chart_orm.original_filename,
        storage_path=chart_orm.storage_path,
        mime_type=chart_orm.mime_type,
        chart_type=chart_orm.chart_type,
        created_at=chart_orm.created_at,
    )


class ChartRepositoryImpl(IChartRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, chart: Chart) -> Chart:
        chart_id = chart.id if chart.id else uuid4()
        now = datetime.utcnow()

        chart_orm = ChartORM(
            id=chart_id,
            study_id=chart.study_id,
            original_filename=chart.original_filename,
            storage_path=chart.storage_path,
            mime_type=chart.mime_type,
            chart_type=chart.chart_type,
            created_at=now,
        )

        self._session.add(chart_orm)
        await self._session.flush()

        return Chart(
            id=chart_orm.id,
            study_id=chart_orm.study_id,
            original_filename=chart_orm.original_filename,
            storage_path=chart_orm.storage_path,
            mime_type=chart_orm.mime_type,
            chart_type=chart_orm.chart_type,
            created_at=chart_orm.created_at,
        )

    async def get_by_id(self, chart_id: UUID) -> Chart | None:
        result = await self._session.execute(
            select(ChartORM).where(ChartORM.id == chart_id)
        )
        chart_orm = result.scalar_one_or_none()
        if not chart_orm:
            return None
        return _orm_to_chart(chart_orm)

    async def list_by_study(
        self, study_id: UUID, limit: int = 100, offset: int = 0
    ) -> list[Chart]:
        result = await self._session.execute(
            select(ChartORM)
            .where(ChartORM.study_id == study_id)
            .order_by(ChartORM.created_at.asc())
            .limit(limit)
            .offset(offset)
        )
        return [_orm_to_chart(c) for c in result.scalars().all()]

    async def count_by_study(self, study_id: UUID) -> int:
        result = await self._session.execute(
            select(func.count()).select_from(ChartORM).where(ChartORM.study_id == study_id)
        )
        return result.scalar() or 0