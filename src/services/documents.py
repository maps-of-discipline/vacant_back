from io import BytesIO
from fastapi import Depends

from src.documents.applications import ApplicationRendered
from src.exceptions.general import EntityNotFoundException
from src.schemas.user import UserSchema
from src.services.applications.transfer import TransferApplicationService


class DocumentService:
    def __init__(
        self,
        renderer: ApplicationRendered = Depends(),
        transfer_service: TransferApplicationService = Depends(),
    ) -> None:
        self._application_renderer = renderer
        self._transfer_service = transfer_service

    async def generate_reinstatement_document(
        self, user: UserSchema, application_id: int
    ) -> BytesIO:
        application = await self._transfer_service.get(application_id)
        if not application:
            raise EntityNotFoundException("Transfer application")

        return self._application_renderer.transfer(user, application)
