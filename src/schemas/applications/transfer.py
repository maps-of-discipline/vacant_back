from src.schemas.applications.application import CreateApplicationSchema


class CreateTransferApplicationSchema(CreateApplicationSchema):
    continue_year: int | None
    paid_policy_accepted: bool


class TransferApplicationSchema(CreateTransferApplicationSchema):
    id: int
    type: str
