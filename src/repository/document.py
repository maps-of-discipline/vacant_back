from fastapi import Depends
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.enums.document import DocumnetTypeEnum
from src.models.db import sessionmaker
from src.models.models import Documents
from src.schemas.document import DocumentSchema, CreateDocumentSchema
from src.logger import get_logger

logger = get_logger(__name__)


class DocumentRepository:
    def __init__(self, session: AsyncSession = Depends(sessionmaker)):
        self.session: AsyncSession = session

    async def create(self, document: CreateDocumentSchema) -> DocumentSchema:
        doc = Documents(**document.model_dump())
        self.session.add(doc)

        await self.session.commit()
        await self.session.refresh(doc)

        logger.debug(
            f"Created document with ID: {doc.id} for application: {doc.application_id}"
        )
        return self._create_schema(doc)

    async def get(self, id: int) -> DocumentSchema | None:
        doc = await self.session.scalar(select(Documents).where(Documents.id == id))
        return self._create_schema(doc) if doc else None

    async def get_by_application_id(self, application_id: int) -> list[DocumentSchema]:
        stmt = select(Documents).where(Documents.application_id == application_id)
        docs = await self.session.scalars(stmt)
        return [self._create_schema(doc) for doc in docs]

    async def delete(self, id: int) -> int | None:
        stmt = delete(Documents).where(Documents.id == id).returning(Documents.id)
        deleted_id = await self.session.scalar(stmt)

        if deleted_id:
            await self.session.commit()
            logger.debug(f"Deleted document with ID: {deleted_id}")

        return deleted_id

    async def delete_by_application_id(self, application_id: int) -> None:
        stmt = delete(Documents).where(Documents.application_id == application_id)
        await self.session.execute(stmt)
        await self.session.commit()
        logger.debug(f"Successfully deleted application[{application_id}]'s documnets")

    def _create_schema(self, doc: Documents) -> DocumentSchema:
        return DocumentSchema(
            id=doc.id,
            application_id=doc.application_id,
            type=DocumnetTypeEnum(doc.type),
            filepath=doc.filepath,
        )

