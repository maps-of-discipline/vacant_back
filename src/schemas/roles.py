from pydantic import BaseModel


class RoleSchema(BaseModel):
    id: int
    title: str
    external_id: str
