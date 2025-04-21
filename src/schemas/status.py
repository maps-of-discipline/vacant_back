from pydantic import BaseModel


class StatusSchema(BaseModel):
    id: int
    title: str
    verbose_name: str


class StatusGetListSchema(BaseModel):
    title: str
    verbose_name: str
    messages: list[str]
