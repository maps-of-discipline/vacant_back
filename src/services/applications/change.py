import hashlib

from fastapi import Depends, UploadFile

from src.exceptions.http import EntityNotFoundHTTPException
from src.repository.document import DocumentRepository
from src.services.file import FileService
from src.repository.applications.change import ChangeApplicationRepository
from src.repository.status import StatusRepository
from src.schemas.applications.change import (
    CreateChangeApplicationSchema,
    ChangeApplicationSchema,
    UpdateChangeApplicationChema,
)
from src.exceptions.general import ItemNotFoundException
from src.logger import get_logger

logger = get_logger(__name__)


class ChangeApplicationService:
    def __init__(
        self,
        repo: ChangeApplicationRepository = Depends(),
        status_repo: StatusRepository = Depends(),
        file_service: FileService = Depends(),
        document_repo: DocumentRepository = Depends(),
    ):
        self._repo = repo
        self._status_repo = status_repo
        self._file_service = file_service
        self._docs_repo = document_repo

    async def create(
        self,
        application: CreateChangeApplicationSchema,
        attachments: list[UploadFile] = [],
    ) -> ChangeApplicationSchema:
        status = await self._status_repo.get_by_title(str(application.status.value))
        if not status:
            raise EntityNotFoundHTTPException("Status")

        created_application = await self._repo.create(application, status.id)

        docs = []
        for file in attachments:
            doc = await self._file_service.upload_document(file, created_application.id)
            docs.append(doc)

        created_application.documents = docs
        return created_application

    async def get(self, id: int) -> ChangeApplicationSchema:
        application = await self._repo.get(id)
        if not application:
            raise ItemNotFoundException(
                f"Change application with id[{id}] doesn't exists."
            )

        documents = await self._docs_repo.get_by_application_id(application.id)
        application.documents = documents
        return application

    async def update(
        self,
        data: UpdateChangeApplicationChema,
        attachments: list[UploadFile] = [],
    ) -> ChangeApplicationSchema:
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
