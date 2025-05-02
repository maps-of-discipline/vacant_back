from fastapi import Depends, UploadFile

from src.exceptions.http import EntityNotFoundHTTPException
from src.repository.applications.transfer import TransferApplicationRepository
from src.repository.document import DocumentRepository
from src.repository.status import StatusRepository
from src.schemas.applications.transfer import (
    CreateTransferApplicationSchema,
    TransferApplicationSchema,
    UpdateTransferApplicationSchema,
)
from src.exceptions.general import ItemNotFoundException
from src.services.file import FileService
from src.logger import get_logger

logger = get_logger(__name__)


class TransferApplicationService:
    def __init__(
        self,
        repo: TransferApplicationRepository = Depends(),
        status_repo: StatusRepository = Depends(),
        file_service: FileService = Depends(),
        docs_repo: DocumentRepository = Depends(),
    ):
        self._repo = repo
        self._status_repo = status_repo
        self._file_service = file_service
        self._docs_repo = docs_repo

    async def create(
        self,
        application: CreateTransferApplicationSchema,
        attachments: list[UploadFile] = [],
    ) -> TransferApplicationSchema:
        status = await self._status_repo.get_by_title(application.status.value)
        if not status:
            logger.error(f"Couldn't find status: {application.status}")
            raise EntityNotFoundHTTPException("Status")

        created_application = await self._repo.create(application, status.id)

        docs = []
        for file in attachments:
            doc = await self._file_service.upload_document(file, created_application.id)
            docs.append(doc)

        created_application.documents = docs
        return created_application

    async def get(self, id: int) -> TransferApplicationSchema:
        application = await self._repo.get(id)
        if application is None:
            raise ItemNotFoundException(
                f"Transfer application with id[{id}] doesn't exists."
            )

        documents = await self._docs_repo.get_by_application_id(application.id)
        application.documents = documents
        return application

    async def update(
        self,
        data: UpdateTransferApplicationSchema,
        attachments: list[UploadFile] = [],
    ) -> TransferApplicationSchema:
        status = await self._status_repo.get_by_title(str(data.status.value))
        if not status:
            raise EntityNotFoundHTTPException("Status")

        application = await self._repo.update(data, status.id)
        if application is None:
            raise EntityNotFoundHTTPException("Chage Application")

        await self._file_service.delete_by_application_id(application.id)

        for attachment in attachments:
            doc = await self._file_service.upload_document(attachment, application.id)
            application.documents.append(doc)

        return application
