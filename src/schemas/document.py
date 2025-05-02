from pydantic import BaseModel

from src.enums import DocumnetTypeEnum


class CreateDocumentSchema(BaseModel):
    application_id: int
    type: DocumnetTypeEnum
    filepath: str


class DocumentSchema(CreateDocumentSchema):
    id: int

