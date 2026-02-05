from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel

from app.domain.models.research_context import ResearchContext

class Study(BaseModel):
    id: UUID
    context: ResearchContext
    status: Literal["draft", "charts_uploaded", "analyzing", "completed", "failed"]
    created_at: datetime
    updated_at: datetime
    failure_reason: str | None = None
    