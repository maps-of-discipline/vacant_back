from pydantic import BaseModel


class CreateDisciplineSchema(BaseModel):
    program_id: int
    title: str
    amount: float
    control: str
    coursework: str
    elective_group: str
    period: int
    zet: int


class DisciplineSchema(CreateDisciplineSchema):
    id: int
