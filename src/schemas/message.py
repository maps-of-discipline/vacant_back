from pydantic import BaseModel


class CommonMessage(BaseModel):
    id: int
    title: str
