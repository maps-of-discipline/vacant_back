from fastapi import Depends

from src.exceptions.http import EntityNotFoundHTTPException
from src.schemas.applications.application import ApplicationForListViewSchema
from src.repository.applications.application import ApplicationRepository


class ApplicationService:
    def __init__(self, repo: ApplicationRepository = Depends()) -> None:
        self._repo = repo

    async def get_all(self, user_id: str) -> list[ApplicationForListViewSchema]:
        applications = await self._repo.all(user_id=user_id)
        return applications

    async def delete(self, application_id: int) -> ApplicationForListViewSchema:
        application = await self._repo.delete(application_id)
        if not application:
            raise EntityNotFoundHTTPException("Application")

        return application
