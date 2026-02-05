from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dto.schemas import ChartInsightItem, ReportResponse
from app.application.use_cases import get_report
from app.infraestructure.repositories import ReportRepositoryImpl
from app.interfaces.api.deps import get_session

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("", response_model=ReportResponse)
async def get_report_by_study(
    study_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    """Obtiene el reporte ejecutivo de un estudio."""
    repo = ReportRepositoryImpl(session)
    report = await get_report(repo, study_id)
    
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    download_url = f"/reports/{report.id}/download" if report.storage_path else None
    
    return ReportResponse(
        id=report.id,
        study_id=report.study_id,
        executive_summary=report.executive_summary,
        chart_insights=[
            ChartInsightItem(chart_id=item.chart_id, insight=item.insight)
            for item in report.chart_insights
        ],
        key_findings=report.key_findings,
        implications=report.implications,
        recommendations=report.recommendations,
        strategies=report.strategies,
        generated_at=report.generated_at,
        download_url=download_url,
    )


@router.get("/{report_id}", response_model=ReportResponse)
async def get_report_by_id(
    report_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    """Obtiene un reporte por su ID."""
    repo = ReportRepositoryImpl(session)
    report = await repo.get_by_id(report_id)
    
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    download_url = f"/reports/{report.id}/download" if report.storage_path else None
    
    return ReportResponse(
        id=report.id,
        study_id=report.study_id,
        executive_summary=report.executive_summary,
        chart_insights=[
            ChartInsightItem(chart_id=item.chart_id, insight=item.insight)
            for item in report.chart_insights
        ],
        key_findings=report.key_findings,
        implications=report.implications,
        recommendations=report.recommendations,
        strategies=report.strategies,
        generated_at=report.generated_at,
        download_url=download_url,
    )