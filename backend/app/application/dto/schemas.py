from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


# ==================== REQUEST ====================

class StudyCreateRequest(BaseModel):
    """Request para crear un estudio con su contexto metodológico."""
    profile: str
    background: str
    business_question: str
    study_type: Literal["quantitative", "qualitative", "mixed"]
    segments: list[str] = Field(default_factory=list)
    sample: str | None = None
    significance_threshold: float | None = None
    models: list[str] = Field(default_factory=list)
    measurements: list[str] = Field(default_factory=list)
    qualitative_study: str | None = None


# ==================== RESPONSE ====================

class StudyResponse(BaseModel):
    """Response al crear o consultar un estudio."""
    id: UUID
    status: str
    created_at: datetime


class StudyDetailResponse(BaseModel):
    """Response con detalle completo del estudio."""
    id: UUID
    status: str
    profile: str
    background: str
    business_question: str
    study_type: str
    segments: list[str]
    sample: str | None
    significance_threshold: float | None
    models: list[str]
    measurements: list[str]
    qualitative_study: str | None
    charts_count: int
    created_at: datetime
    updated_at: datetime
    failure_reason: str | None = None


class ChartItem(BaseModel):
    """Información de una gráfica subida."""
    id: UUID
    original_filename: str
    mime_type: str
    created_at: datetime


class ChartsUploadResponse(BaseModel):
    """Response al subir gráficas."""
    study_id: UUID
    charts: list[ChartItem]


class AnalyzeAcceptedResponse(BaseModel):
    """Response al lanzar análisis."""
    study_id: UUID
    status: str
    message: str


class ChartInsightItem(BaseModel):
    """Insight de una gráfica en el reporte."""
    chart_id: UUID
    insight: str


class ReportResponse(BaseModel):
    """Response con el reporte ejecutivo."""
    id: UUID
    study_id: UUID
    executive_summary: str
    chart_insights: list[ChartInsightItem]
    key_findings: list[str]
    implications: list[str]
    recommendations: list[str]
    strategies: list[str]
    generated_at: datetime
    download_url: str | None = None