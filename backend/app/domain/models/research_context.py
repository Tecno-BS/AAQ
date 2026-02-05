from typing import Literal

from pydantic import BaseModel, Field

class ResearchContext(BaseModel):
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
