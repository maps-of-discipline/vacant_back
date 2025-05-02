import hashlib

from fastapi import Depends, UploadFile
from typing import Optional

from src.exceptions.http import EntityNotFoundHTTPException
from src.repository.document import DocumentRepository
from src.schemas.document import DocumentSchema, CreateDocumentSchema
from src.utils.files import BaseFileHandler, LocalFileHandler
from src.enums import DocumnetTypeEnum
from src.logger import get_logger

logger = get_logger(__name__)


class FileService:
    def __init__(
        self,
        document_repo: DocumentRepository = Depends(),
        file_handler: BaseFileHandler = Depends(LocalFileHandler),
    ):
        self._document_repo = document_repo
        self._file_handler = file_handler

    async def upload_document(
        self, file: UploadFile, application_id: int
    ) -> DocumentSchema:
        if not file.filename:
            raise Exception("Uploaded file dont have filename")

        await file.seek(0)
        file_content = await file.read()
        hash = hashlib.md5(file_content).hexdigest()
        logger.debug(f"{file.filename} hash: {hash}")

        (doc_type, fname) = file.filename.split("-", 1)
        doc_type = DocumnetTypeEnum(doc_type)

        doc_schema = CreateDocumentSchema(
            application_id=application_id,
            type=doc_type,
            filepath=self._file_handler.get_file_path(application_id, doc_type, fname),
        )

        document = await self._document_repo.create(doc_schema)
        await self._file_handler.save(document, file_content)
        logger.info(f"File {doc_schema.filepath} saved successfully")
        return document

    async def get_document_file(
        self, document_id: int
    ) -> tuple[Optional[str], Optional[bytes]]:
        document = await self._document_repo.get(document_id)
        if not document:
            raise EntityNotFoundHTTPException("Document")

        content = await self._file_handler.get(document)
        if not content:
            return None, None

        filename = (
            document.filepath.split("/")[-1]
            if document.filepath
            else f"document-{document_id}"
        )

        return filename, content

    async def delete_document(self, document_id: int) -> bool:
        document = await self._document_repo.get(document_id)
        if not document:
            raise EntityNotFoundHTTPException("Document")

        await self._file_handler.delete(document)
        doc_deleted = await self._document_repo.delete(document_id)

        return doc_deleted is not None

    async def delete_by_application_id(self, application_id: int):
        await self._document_repo.delete_by_application_id(application_id)
        await self._file_handler.delete_by_application_id(application_id)
