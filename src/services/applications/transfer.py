from fastapi import Depends

from src.repository.applications.transfer import TransferApplicationRepository
from src.schemas.applications.transfer import (
    CreateTransferApplicationSchema,
    TransferApplicationSchema,
)
from src.exceptions.general import ItemNotFoundException


class TransferApplicationService:
    def __init__(self, repo: TransferApplicationRepository = Depends()):
        self._repo = repo

    async def create(
        self, application: CreateTransferApplicationSchema
    ) -> TransferApplicationSchema:
        created_application = await self._repo.create(application)
        return created_application

    async def get(self, id: int) -> TransferApplicationSchema:
        application = await self._repo.get(id)
        if application is None:
            raise ItemNotFoundException(
                f"Transfer application with id[{id}] doesn't exists."
            )
        return application
