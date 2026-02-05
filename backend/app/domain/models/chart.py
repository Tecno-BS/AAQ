from ast import Store
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

class Chart(BaseModel):
    id: UUID
    study_id: UUID
    original_filename: str
    storage_path: str
    mime_type: str
    chart_type: str | None = None
    created_at: datetime

    