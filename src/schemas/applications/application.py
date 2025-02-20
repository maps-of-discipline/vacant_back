from datetime import datetime

from pydantic import BaseModel, ConfigDict


from src.schemas.user import UserForListViewSchema


class CreateProgramSchema(BaseModel):
    type: str
    application_id: int
    priority: int | None
    okso: str
    profile: str
    form: str | None
    base: str | None
    sem_num: int | None
    university: str

    model_config = ConfigDict(from_attributes=True)


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

    model_config = ConfigDict(from_attributes=True)


class ApplicationForListViewSchema(BaseModel):
    id: int
    date: datetime
    user: UserForListViewSchema

    hostel_policy_accepted: bool
    vacation_policy_viewed: bool
    no_restrictions_policy_accepted: bool
    reliable_information_policy_accepted: bool
