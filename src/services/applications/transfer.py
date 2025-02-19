from fastapi import Depends

from src.repository.applications.transfer import TransferApplicationRepository
from src.schemas.applications.transfer import (
    CreateTransferApplicationSchema,
    TransferApplicationSchema,
)


class TransferApplicationService:
    def __init__(self, repo: TransferApplicationRepository = Depends()):
        self._repo = repo

    async def create(
        self, application: CreateTransferApplicationSchema
    ) -> TransferApplicationSchema:
        created_application = await self._repo.create(application)
        return created_application
