from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.models import Chart

class IChartRepository(ABC):
    @abstractmethod
    async def create(self, chart: Chart) -> Chart:
        pass

    @abstractmethod
    async def get_by_id(self, chart_id: UUID) -> Chart | None:
        pass

    @abstractmethod
    async def list_by_study(
        self, study_id: UUID, limit: int = 100, offset: int = 0
    ) -> list[Chart]:
        pass

    @abstractmethod
    async def count_by_study(self, study_id: UUID) -> int:
        pass

    