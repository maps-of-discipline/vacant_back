from fastapi import Depends

from src.schemas.applications.application import ApplicationForListViewSchema
from src.repository.applications.application import ApplicationRepository


class ApplicationService:
    def __init__(self, repo: ApplicationRepository = Depends()) -> None:
        self._repo = repo

    async def get_all(self) -> list[ApplicationForListViewSchema]:
        applications = await self._repo.all()
        return applications
