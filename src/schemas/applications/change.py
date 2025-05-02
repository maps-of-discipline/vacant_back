from pydantic import Field
from src.schemas.applications.application import CreateApplicationSchema, ProgramSchema
from src.enums import ApplicationStatusEnum
from src.schemas.document import DocumentSchema


class RequestCreateChangeApplicationSchema(CreateApplicationSchema):
    purpose: str


class CreateChangeApplicationSchema(RequestCreateChangeApplicationSchema):
    user_id: str


class ChangeApplicationSchema(CreateChangeApplicationSchema):
    id: int
    type: str
    programs: list[ProgramSchema]
    status: ApplicationStatusEnum
    documents: list[DocumentSchema] = Field(default_factory=list)


class UpdateChangeApplicationChema(ChangeApplicationSchema): ...
