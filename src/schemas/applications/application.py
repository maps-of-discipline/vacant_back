from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CreateProgramSchema(BaseModel):
    type: str
    okso: str
    profile: str
    form: str | None
    base: str | None
    sem_num: int | None
    university: str

    model_config = ConfigDict(from_attributes=True)


class ProgramSchema(CreateProgramSchema):
    id: int
    application_id: int


class CreateApplicationSchema(BaseModel):
    date: datetime

    hostel_policy_accepted: bool
    vacation_policy_viewed: bool
    no_restrictions_policy_accepted: bool
    reliable_information_policy_accepted: bool

    programs: list[CreateProgramSchema]

    model_config = ConfigDict(from_attributes=True)


class ApplicationForListViewSchema(BaseModel):
    id: int
    date: datetime
    type: str
    status: str

    hostel_policy_accepted: bool
    vacation_policy_viewed: bool
    no_restrictions_policy_accepted: bool
    reliable_information_policy_accepted: bool


class DeleteApplicationRequestSchema(BaseModel):
    id: int
