from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

class ChartInsightItem(BaseModel):
    chart_id: UUID
    insight: str

class ExecutiveReport(BaseModel):
    id: UUID
    study_id: UUID
    executive_summary: str
    chart_insights: list[ChartInsightItem] = Field(default_factory=list)
    key_findings: list[str] = Field(default_factory=list)
    implications: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    strategies: list[str] = Field(default_factory=list)
    generated_at: datetime
    report_format: Literal["pdf", "docx"] | None = None
    storage_path: str | None = None
    