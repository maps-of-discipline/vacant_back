from src.schemas.applications.application import CreateApplicationSchema


class RequestCreateTransferApplicationSchema(CreateApplicationSchema):
    continue_year: int | None
    paid_policy_accepted: bool


class CreateTransferApplicationSchema(RequestCreateTransferApplicationSchema):
    user_id: str


class TransferApplicationSchema(CreateTransferApplicationSchema):
    id: int
    type: str
    status: str
