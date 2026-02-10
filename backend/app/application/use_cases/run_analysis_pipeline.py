"""Ejecuta el pipeline cognitivo y persiste resultados."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models import ChartInsightItem, ExecutiveReport
from app.infraestructure.graphs.pipeline import build_pipeline_graph
from app.infraestructure.graphs.state import PipelineState
from app.infraestructure.repositories import (
    AnalysisRepositoryImpl,
    ChartRepositoryImpl,
    ReportRepositoryImpl,
    StudyRepositoryImpl,
)


async def run_analysis_pipeline(
    session: AsyncSession,
    study_id: UUID,
) -> dict:
    study_repo = StudyRepositoryImpl(session)
    chart_repo = ChartRepositoryImpl(session)
    analysis_repo = AnalysisRepositoryImpl(session)
    report_repo = ReportRepositoryImpl(session)

    study = await study_repo.get_by_id(study_id)
    if not study:
        raise ValueError("Study not found")

    charts = await chart_repo.list_by_study(study_id)
    if not charts:
        raise ValueError("No charts uploaded")

    initial_state: PipelineState = {
        "study_id": str(study_id),
        "study": study,
        "context": study.context,
        "charts": charts,
    }

    graph = build_pipeline_graph()
    final_state = await graph.ainvoke(initial_state)

    if final_state.get("status") == "failed":
        await study_repo.update_status(
            study_id, "failed", final_state.get("error", "Unknown error")
        )
        return {"status": "failed", "error": final_state.get("error")}

    analyses = final_state.get("chart_analyses", [])
    for a in analyses:
        a.id = uuid4()
        a.study_id = study_id
        await analysis_repo.create(a)

    chart_insights = [
        ChartInsightItem(chart_id=a.chart_id, insight=a.explanation[:200])
        for a in analyses
    ]

    report = ExecutiveReport(
        id=uuid4(),
        study_id=study_id,
        executive_summary=final_state.get("executive_summary", ""),
        chart_insights=chart_insights,
        key_findings=final_state.get("key_findings", []),
        implications=[],
        recommendations=final_state.get("recommendations", []),
        strategies=final_state.get("strategies", []),
        generated_at=datetime.utcnow(),
    )
    await report_repo.create(report)

    await study_repo.update_status(study_id, "completed")

    return {"status": "completed", "report_id": str(report.id)}