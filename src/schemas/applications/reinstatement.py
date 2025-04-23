from src.schemas.applications.application import CreateApplicationSchema, ProgramSchema
from pydantic import ConfigDict


class RequestCreateReinstatementApplicationSchema(CreateApplicationSchema):
    is_vacation_need: bool
    begin_year: int
    end_year: int
    purpose: str

    paid_policy_accepted: bool


class CreateReinstatementApplicationSchema(RequestCreateReinstatementApplicationSchema):
    user_id: str


class ReinstatementApplicationSchema(CreateReinstatementApplicationSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int
    type: str
    programs: list[ProgramSchema]


class UpdateReinstatementApplicationSchema(ReinstatementApplicationSchema): ...
