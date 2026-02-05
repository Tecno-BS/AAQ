from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models import ChartInsightItem, ExecutiveReport
from app.domain.repositories import IReportRepository
from app.infraestructure.db.models import ReportORM


def _orm_to_report(report_orm: ReportORM) -> ExecutiveReport:
    # Convertir chart_insights de list[dict] a list[ChartInsightItem]
    chart_insights = []
    for item in report_orm.chart_insights or []:
        chart_insights.append(
            ChartInsightItem(
                chart_id=item["chart_id"],
                insight=item["insight"],
            )
        )

    return ExecutiveReport(
        id=report_orm.id,
        study_id=report_orm.study_id,
        executive_summary=report_orm.executive_summary,
        chart_insights=chart_insights,
        key_findings=report_orm.key_findings or [],
        implications=report_orm.implications or [],
        recommendations=report_orm.recommendations or [],
        strategies=report_orm.strategies or [],
        generated_at=report_orm.generated_at,
        report_format=report_orm.report_format,
        storage_path=report_orm.storage_path,
    )


class ReportRepositoryImpl(IReportRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, report: ExecutiveReport) -> ExecutiveReport:
        report_id = report.id if report.id else uuid4()
        now = datetime.utcnow()

        # Convertir chart_insights a list[dict] para JSONB
        chart_insights_data = [
            {"chart_id": str(item.chart_id), "insight": item.insight}
            for item in report.chart_insights
        ]

        report_orm = ReportORM(
            id=report_id,
            study_id=report.study_id,
            executive_summary=report.executive_summary,
            chart_insights=chart_insights_data,
            key_findings=report.key_findings,
            implications=report.implications,
            recommendations=report.recommendations,
            strategies=report.strategies,
            generated_at=now,
            report_format=report.report_format,
            storage_path=report.storage_path,
        )

        self._session.add(report_orm)
        await self._session.flush()

        return ExecutiveReport(
            id=report_orm.id,
            study_id=report_orm.study_id,
            executive_summary=report_orm.executive_summary,
            chart_insights=report.chart_insights,
            key_findings=report_orm.key_findings or [],
            implications=report_orm.implications or [],
            recommendations=report_orm.recommendations or [],
            strategies=report_orm.strategies or [],
            generated_at=report_orm.generated_at,
            report_format=report_orm.report_format,
            storage_path=report_orm.storage_path,
        )

    async def get_by_id(self, report_id: UUID) -> ExecutiveReport | None:
        result = await self._session.execute(
            select(ReportORM).where(ReportORM.id == report_id)
        )
        report_orm = result.scalar_one_or_none()
        if not report_orm:
            return None
        return _orm_to_report(report_orm)

    async def get_by_study(self, study_id: UUID) -> ExecutiveReport | None:
        result = await self._session.execute(
            select(ReportORM).where(ReportORM.study_id == study_id)
        )
        report_orm = result.scalar_one_or_none()
        if not report_orm:
            return None
        return _orm_to_report(report_orm)

    async def update(self, report: ExecutiveReport) -> ExecutiveReport:
        result = await self._session.execute(
            select(ReportORM).where(ReportORM.id == report.id)
        )
        report_orm = result.scalar_one_or_none()
        if not report_orm:
            raise ValueError(f"Report {report.id} not found")

        chart_insights_data = [
            {"chart_id": str(item.chart_id), "insight": item.insight}
            for item in report.chart_insights
        ]

        report_orm.executive_summary = report.executive_summary
        report_orm.chart_insights = chart_insights_data
        report_orm.key_findings = report.key_findings
        report_orm.implications = report.implications
        report_orm.recommendations = report.recommendations
        report_orm.strategies = report.strategies
        report_orm.report_format = report.report_format
        report_orm.storage_path = report.storage_path

        await self._session.flush()
        return report

    async def update_storage(
        self, report_id: UUID, storage_path: str, report_format: str
    ) -> None:
        result = await self._session.execute(
            select(ReportORM).where(ReportORM.id == report_id)
        )
        report_orm = result.scalar_one_or_none()
        if not report_orm:
            raise ValueError(f"Report {report_id} not found")

        report_orm.storage_path = storage_path
        report_orm.report_format = report_format
        await self._session.flush()