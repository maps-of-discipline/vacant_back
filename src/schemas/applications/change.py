from datetime import datetime

from pydantic import ConfigDict

from src.schemas.applications.application import CreateApplicationSchema, ProgramSchema


class RequestCreateChangeApplicationSchema(CreateApplicationSchema):
    purpose: str


class CreateChangeApplicationSchema(RequestCreateChangeApplicationSchema):
    user_id: str


class ChangeApplicationSchema(CreateChangeApplicationSchema):
    id: int
    type: str
    programs: list[ProgramSchema]


class UpdateChangeApplicationChema(ChangeApplicationSchema): ...
