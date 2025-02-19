from fastapi import Depends

from src.repository.applications.reinstatement import ReinstatementApplicationRepository
from src.schemas.applications.reinstatement import (
    CreateReinstatementApplicationSchema,
    ReinstatementApplicationSchema,
)
from src.exceptions.general import ItemNotFoundException


class ReinstatementApplicationService:
    def __init__(self, repo: ReinstatementApplicationRepository = Depends()):
        self._repo = repo

    async def create(
        self, application: CreateReinstatementApplicationSchema
    ) -> ReinstatementApplicationSchema:
        created_application = await self._repo.create(application)
        return created_application

    async def get(self, id: int) -> ReinstatementApplicationSchema:
        application = await self._repo.get(id)
        if application is None:
            raise ItemNotFoundException(
                f"Change application with id[{id}] doesn't exists."
            )
        return application
