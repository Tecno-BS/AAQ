import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infraestructure.db.base import Base


class StudyORM(Base):
    __tablename__ = "studies"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="draft")
    failure_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relaciones
    context: Mapped["ResearchContextORM"] = relationship(
        back_populates="study", uselist=False, cascade="all, delete-orphan"
    )
    charts: Mapped[list["ChartORM"]] = relationship(
        back_populates="study", cascade="all, delete-orphan"
    )
    analyses: Mapped[list["AnalysisORM"]] = relationship(
        back_populates="study", cascade="all, delete-orphan"
    )
    report: Mapped["ReportORM | None"] = relationship(
        back_populates="study", uselist=False, cascade="all, delete-orphan"
    )


class ResearchContextORM(Base):
    __tablename__ = "research_contexts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    study_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("studies.id", ondelete="CASCADE"),
        nullable=False,
    )
    profile: Mapped[str] = mapped_column(String(500), nullable=False)
    background: Mapped[str] = mapped_column(Text, nullable=False)
    business_question: Mapped[str] = mapped_column(Text, nullable=False)
    study_type: Mapped[str] = mapped_column(String(50), nullable=False)
    segments: Mapped[list] = mapped_column(JSONB, default=list)
    sample: Mapped[str | None] = mapped_column(Text, nullable=True)
    significance_threshold: Mapped[float | None] = mapped_column(Float, nullable=True)
    models: Mapped[list] = mapped_column(JSONB, default=list)
    measurements: Mapped[list] = mapped_column(JSONB, default=list)
    qualitative_study: Mapped[str | None] = mapped_column(Text, nullable=True)

    study: Mapped["StudyORM"] = relationship(back_populates="context")


class ChartORM(Base):
    __tablename__ = "charts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    study_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("studies.id", ondelete="CASCADE"),
        nullable=False,
    )
    original_filename: Mapped[str] = mapped_column(String(500), nullable=False)
    storage_path: Mapped[str] = mapped_column(String(1000), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    chart_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )

    study: Mapped["StudyORM"] = relationship(back_populates="charts")
    analysis: Mapped["AnalysisORM | None"] = relationship(
        back_populates="chart", uselist=False, cascade="all, delete-orphan"
    )


class AnalysisORM(Base):
    __tablename__ = "analyses"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    chart_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("charts.id", ondelete="CASCADE"),
        nullable=False,
    )
    study_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("studies.id", ondelete="CASCADE"),
        nullable=False,
    )
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    hypotheses: Mapped[list] = mapped_column(JSONB, default=list)
    business_impact: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )

    chart: Mapped["ChartORM"] = relationship(back_populates="analysis")
    study: Mapped["StudyORM"] = relationship(back_populates="analyses")


class ReportORM(Base):
    __tablename__ = "reports"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    study_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("studies.id", ondelete="CASCADE"),
        nullable=False,
    )
    executive_summary: Mapped[str] = mapped_column(Text, nullable=False)
    chart_insights: Mapped[list] = mapped_column(JSONB, default=list)
    key_findings: Mapped[list] = mapped_column(JSONB, default=list)
    implications: Mapped[list] = mapped_column(JSONB, default=list)
    recommendations: Mapped[list] = mapped_column(JSONB, default=list)
    strategies: Mapped[list] = mapped_column(JSONB, default=list)
    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    report_format: Mapped[str | None] = mapped_column(String(20), nullable=True)
    storage_path: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    study: Mapped["StudyORM"] = relationship(back_populates="report")