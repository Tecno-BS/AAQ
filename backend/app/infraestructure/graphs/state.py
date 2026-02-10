#Estados del pipeline hecho en LangGraph

from typing import Any, TypedDict
from app.domain.models import Chart, ChartAnalysis, ExecutiveReport, ResearchContext, Study

class PipelineState(TypedDict, total=False):
    #Estado que fluye entre los nodos del grafo.

    study_id : str
    study : Study
    context : ResearchContext
    charts : list[Chart]
    chart_analyses : list[ChartAnalysis]
    hypotheses : list[str]
    key_findings : list[str]
    executive_summary : str
    recommendations : list[str]
    strategies : list[str]
    report : ExecutiveReport
    error : str
    status : str # "validating" | "classifying" | "analyzing" | "synthesizing" | "completed" | "failed"