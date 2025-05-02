from pydantic import Field
from src.schemas.applications.application import CreateApplicationSchema, ProgramSchema
from src.enums import ApplicationStatusEnum
from src.schemas.document import DocumentSchema


class RequestCreateTransferApplicationSchema(CreateApplicationSchema):
    continue_year: int | None
    paid_policy_accepted: bool


class CreateTransferApplicationSchema(RequestCreateTransferApplicationSchema):
    user_id: str


class TransferApplicationSchema(CreateTransferApplicationSchema):
    id: int
    type: str
    programs: list[ProgramSchema]
    status: ApplicationStatusEnum
    documents: list[DocumentSchema] = Field(default_factory=list)


class UpdateTransferApplicationSchema(TransferApplicationSchema): ...
