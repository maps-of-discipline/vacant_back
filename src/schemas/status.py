from pydantic import BaseModel

from src.schemas.message import CommonMessage


class StatusSchema(BaseModel):
    id: int
    title: str
    verbose_name: str


class StatusGetListSchema(BaseModel):
    title: str
    verbose_name: str
    messages: list[CommonMessage]
