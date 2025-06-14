from pydantic import BaseModel


class GetSolutionRequestSchema(BaseModel):
    application_id: int
    program_type: str

