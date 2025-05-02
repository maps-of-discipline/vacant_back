from src.schemas.applications.application import CreateApplicationSchema, ProgramSchema
from pydantic import ConfigDict, Field
from src.enums import ApplicationStatusEnum
from src.schemas.document import DocumentSchema


class RequestCreateReinstatementApplicationSchema(CreateApplicationSchema):
    is_vacation_need: bool
    begin_year: int
    end_year: int
    purpose: str

    paid_policy_accepted: bool


class CreateReinstatementApplicationSchema(RequestCreateReinstatementApplicationSchema):
    user_id: str


class ReinstatementApplicationSchema(CreateReinstatementApplicationSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int
    type: str
    programs: list[ProgramSchema]
    status: ApplicationStatusEnum
    documents: list[DocumentSchema] = Field(default_factory=list)


class UpdateReinstatementApplicationSchema(ReinstatementApplicationSchema): ...
