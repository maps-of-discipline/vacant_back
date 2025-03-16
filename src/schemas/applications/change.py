from datetime import datetime

from pydantic import ConfigDict

from src.schemas.applications.application import CreateApplicationSchema


class POSTCreateChangeApplicationSchema(CreateApplicationSchema):
    purpose: str


class CreateChangeApplicationSchema(POSTCreateChangeApplicationSchema):
    user_id: int


class ChangeApplicationSchema(CreateChangeApplicationSchema):
    id: int
    type: str
