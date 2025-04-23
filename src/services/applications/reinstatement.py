from fastapi import Depends

from src.exceptions.http import EntityNotFoundHTTPException
from src.repository.applications.reinstatement import ReinstatementApplicationRepository
from src.repository.status import StatusRepository
from src.schemas.applications.reinstatement import (
    CreateReinstatementApplicationSchema,
    ReinstatementApplicationSchema,
    UpdateReinstatementApplicationSchema,
)
from src.exceptions.general import ItemNotFoundException
from src.logger import get_logger

logger = get_logger(__name__)


class ReinstatementApplicationService:
    def __init__(
        self,
        repo: ReinstatementApplicationRepository = Depends(),
        status_repo: StatusRepository = Depends(),
    ):
        self._repo = repo
        self._status_repo = status_repo

    async def create(
        self, application: CreateReinstatementApplicationSchema
    ) -> ReinstatementApplicationSchema:
        status = await self._status_repo.get_by_title(application.status.value)
        if not status:
            raise EntityNotFoundHTTPException("Status")

        created_application = await self._repo.create(application, status.id)
        return created_application

    async def get(self, id: int) -> ReinstatementApplicationSchema:
        application = await self._repo.get(id)
        if application is None:
            raise ItemNotFoundException(
                f"Change application with id[{id}] doesn't exists."
            )
        return application

    async def update(
        self, data: UpdateReinstatementApplicationSchema
    ) -> ReinstatementApplicationSchema:
        status = await self._status_repo.get_by_title(str(data.status.value))
        if not status:
            raise EntityNotFoundHTTPException("Status")

        application = await self._repo.update(data, status.id)
        if application is None:
            raise EntityNotFoundHTTPException("Chage Application")

        return application
