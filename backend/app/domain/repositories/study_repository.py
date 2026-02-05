from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.models import Study

class IStudyRepository(ABC):
    @abstractmethod
    async def create(self, study: Study) -> Study:
        pass
    
    @abstractmethod
    async def get_by_id(self, study_id: UUID) -> Study | None:
        pass

    @abstractmethod
    async def update(self, study: Study) -> Study:
        pass

    @abstractmethod
    async def update_status(
        self, study_id: UUID, status: str, failure_reason: str | None = None
    ) -> None:
        pass

    @abstractmethod
    async def list(self, limit: int = 50, offset: int = 0) -> list[Study]:
        pass