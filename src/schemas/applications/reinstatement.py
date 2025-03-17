from src.schemas.applications.application import CreateApplicationSchema
from pydantic import ConfigDict


class RequestCreateReinstatementApplicationSchema(CreateApplicationSchema):
    is_vacation_need: bool
    begin_year: int
    end_year: int
    purpose: str

    paid_policy_accepted: bool


class CreateReinstatementApplicationSchema(RequestCreateReinstatementApplicationSchema):
    user_id: int


class ReinstatementApplicationSchema(CreateReinstatementApplicationSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int
    type: str
    status: str
