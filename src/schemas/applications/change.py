from datetime import datetime

from src.schemas.applications.application import CreateApplicationSchema


class CreateChangeApplicationSchema(CreateApplicationSchema):
    change_date: datetime
    purpose: str


class ChangeApplicationSchema(CreateChangeApplicationSchema):
    id: int
    type: str

