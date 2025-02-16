from datetime import datetime

from pydantic import BaseModel, conlist


class CreateProgramSchema(BaseModel):
    type: str
    priority: int | None
    okso: str
    profile: str
    form: str | None
    base: str | None
    sem_num: int | None
    university: str


class ProgramSchema(CreateProgramSchema):
    id: int


class CreateApplicationSchema(BaseModel):
    user_id: int
    date: datetime

    hostel_policy_accepted: bool
    vacation_policy_viewed: bool
    no_restrictions_policy_accepted: bool
    reliable_information_policy_accepted: bool

    programs: list[CreateProgramSchema]



