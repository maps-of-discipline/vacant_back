from src.schemas.applications.application import CreateApplicationSchema
from pydantic import ConfigDict


class CreateReinstatementApplicationSchema(CreateApplicationSchema):
    is_vacation_need: bool
    begin_year: int
    end_year: int
    purpose: str

    paid_policy_accepted: bool


class ReinstatementApplicationSchema(CreateReinstatementApplicationSchema):
    model_config = ConfigDict(
        from_attributes=True
    )
    id: int
    type: str

