from pydantic import BaseModel


class GetRupDataAup(BaseModel):
    num: str
    sem: int


class GetRupDataSchema(BaseModel):
    source: GetRupDataAup
    target: GetRupDataAup
