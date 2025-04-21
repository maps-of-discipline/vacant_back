from fastapi import Depends

from src.exceptions.http import EntityNotFoundHTTPException
from src.repository.applications.transfer import TransferApplicationRepository
from src.repository.status import StatusRepository
from src.schemas.applications.transfer import (
    CreateTransferApplicationSchema,
    TransferApplicationSchema,
)
from src.exceptions.general import ItemNotFoundException


class TransferApplicationService:
    def __init__(
        self,
        repo: TransferApplicationRepository = Depends(),
        status_repo: StatusRepository = Depends(),
    ):
        self._repo = repo
        self._status_repo = status_repo

    async def create(
        self, application: CreateTransferApplicationSchema
    ) -> TransferApplicationSchema:
        status = await self._status_repo.get_by_title(application.status)
        if not status:
            raise EntityNotFoundHTTPException("Status")

        created_application = await self._repo.create(application, status.id)
        return created_application

    async def get(self, id: int) -> TransferApplicationSchema:
        application = await self._repo.get(id)
        if application is None:
            raise ItemNotFoundException(
                f"Transfer application with id[{id}] doesn't exists."
            )
        return application
