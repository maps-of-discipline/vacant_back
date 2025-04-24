from src.schemas.applications.application import CreateApplicationSchema, ProgramSchema
from src.enums import ApplicationStatusEnum


class RequestCreateChangeApplicationSchema(CreateApplicationSchema):
    purpose: str


class CreateChangeApplicationSchema(RequestCreateChangeApplicationSchema):
    user_id: str


class ChangeApplicationSchema(CreateChangeApplicationSchema):
    id: int
    type: str
    programs: list[ProgramSchema]
    status: ApplicationStatusEnum


class UpdateChangeApplicationChema(ChangeApplicationSchema): ...
