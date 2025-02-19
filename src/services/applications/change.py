from fastapi import Depends

from src.repository.applications.change import ChangeApplicationRepository
from src.schemas.applications.change import (
    CreateChangeApplicationSchema,
    ChangeApplicationSchema,
)
from src.exceptions.general import ItemNotFoundException


class ChangeApplicationService:
    def __init__(self, repo: ChangeApplicationRepository = Depends()):
        self._repo = repo

    async def create(
        self, application: CreateChangeApplicationSchema
    ) -> ChangeApplicationSchema:
        created_application = await self._repo.create(application)
        return created_application

    async def get(self, id: int) -> ChangeApplicationSchema:
        application = await self._repo.get(id)
        if not application:
            raise ItemNotFoundException(
                f"Change application with id[{id}] doesn't exists."
            )
        return application
