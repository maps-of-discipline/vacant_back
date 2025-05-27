from io import BytesIO
from fastapi import Depends

from src.documents.applications import ApplicationRendered
from src.exceptions.general import EntityNotFoundException
from src.schemas.user import UserSchema
from src.repository.applications.reinstatement import ReinstatementApplicationRepository
from src.repository.applications.change import ChangeApplicationRepository
from src.repository.applications.transfer import TransferApplicationRepository


class DocumentService:
    def __init__(
        self,
        renderer: ApplicationRendered = Depends(),
        transfer_repo: TransferApplicationRepository = Depends(),
        reinstatement_repo: ReinstatementApplicationRepository = Depends(),
        change_repo: ChangeApplicationRepository = Depends(),
    ) -> None:
        self._application_renderer = renderer
        self._transfer_repo = transfer_repo
        self._change_repo = change_repo
        self._reinstatement_repo = reinstatement_repo

    async def generate_transfer_document(
        self, user: UserSchema, application_id: int
    ) -> BytesIO:
        application = await self._transfer_repo.get(application_id)
        if not application:
            raise EntityNotFoundException("Transfer application")

        return self._application_renderer.transfer(user, application)
    
    async def generate_reinstatement_document(
        self, user: UserSchema, application_id: int
    ) -> BytesIO:
        application = await self._reinstatement_repo.get(application_id)
        if not application:
            raise EntityNotFoundException("Reinstatement application")

        return self._application_renderer.reainstatement(user, application)
    
    async def generate_change_document(
        self, user: UserSchema, application_id: int
    ) -> BytesIO:
        application = await self._change_repo.get(application_id)
        if not application:
            raise EntityNotFoundException("Transfer application")

        return self._application_renderer.change(user, application)
