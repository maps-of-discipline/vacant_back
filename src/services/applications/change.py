from fastapi import Depends

from src.exceptions.http import EntityNotFoundHTTPException
from src.repository.applications.change import ChangeApplicationRepository
from src.repository.status import StatusRepository
from src.schemas.applications.change import (
    CreateChangeApplicationSchema,
    ChangeApplicationSchema,
)
from src.exceptions.general import ItemNotFoundException


class ChangeApplicationService:
    def __init__(
        self,
        repo: ChangeApplicationRepository = Depends(),
        status_repo: StatusRepository = Depends(),
    ):
        self._repo = repo
        self._status_repo = status_repo

    async def create(
        self, application: CreateChangeApplicationSchema
    ) -> ChangeApplicationSchema:
        status = await self._status_repo.get_by_title(application.status)
        if not status:
            raise EntityNotFoundHTTPException("Status")

        created_application = await self._repo.create(application, status.id)
        return created_application

    async def get(self, id: int) -> ChangeApplicationSchema:
        application = await self._repo.get(id)
        if not application:
            raise ItemNotFoundException(
                f"Change application with id[{id}] doesn't exists."
            )
        return application
