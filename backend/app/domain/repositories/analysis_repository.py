from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.models import ChartAnalysis

class IAnalysisRepository(ABC):
    @abstractmethod
    async def create(self, analysis: ChartAnalysis) -> ChartAnalysis:
        pass

    @abstractmethod
    async def get_by_id(self, analysis_id: UUID) -> ChartAnalysis | None:
        pass

    @abstractmethod
    async def get_by_chart(self, chart_id: UUID) -> ChartAnalysis | None:
        pass

    @abstractmethod
    async def list_by_study(
        self, study_id: UUID, limit: int = 100, offset: int = 0
    ) -> list[ChartAnalysis]:
        pass

    