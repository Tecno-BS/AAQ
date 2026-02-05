from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.models import ExecutiveReport

class IReportRepository(ABC):
    @abstractmethod
    async def create(self, report: ExecutiveReport) -> ExecutiveReport:
        pass

    @abstractmethod
    async def get_by_id(self, report_id: UUID) -> ExecutiveReport | None:
        pass

    @abstractmethod
    async def get_by_study(self, study_id: UUID) -> ExecutiveReport | None:
        pass

    @abstractmethod
    async def update_storage(
        self, report_id: UUID, storage_path: str, report_format: str
    ) -> None:
        pass