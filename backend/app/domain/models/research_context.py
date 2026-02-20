from pydantic import BaseModel, Field

from app.core.constants import STUDY_TYPES

class ResearchContext(BaseModel):
    profile: str
    background: str
    business_question: str
    study_type: str
    segments: list[str] = Field(default_factory=list)
    sample: str | None = None
    significance_threshold: float | None = None
    models: list[str] = Field(default_factory=list)
    measurements: list[str] = Field(default_factory=list)
    qualitative_study: str | None = None

    @model_validator(mode="after")
    def validate_study_type(self):
        if self.study_type not in STUDY_TYPES:
            raise ValueError(
                f"study_type debe ser uno de los tipos oficiales."
                f"Recibido: '{self.study_type}'"
            )

        return self
        