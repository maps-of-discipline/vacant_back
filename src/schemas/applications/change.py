from datetime import datetime

from pydantic import ConfigDict

from src.schemas.applications.application import CreateApplicationSchema


class RequestCreateChangeApplicationSchema(CreateApplicationSchema):
    purpose: str


class CreateChangeApplicationSchema(RequestCreateChangeApplicationSchema):
    user_id: int


class ChangeApplicationSchema(CreateChangeApplicationSchema):
    id: int
    type: str
