from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

class ChartAnalysis(BaseModel):
    id: UUID
    chart_id: UUID
    study_id: UUID
    explanation: str
    hypotheses: list[str] = Field(default_factory=list)
    business_impact: str | None = None
    created_at: datetime

