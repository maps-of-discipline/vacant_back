from pydantic import BaseModel

from src.enums.comment import CommentScopeEnum


class CommentSchema(BaseModel):
    id: int
    text: str


class GetApplicationCommentsRequestSchema(BaseModel):
    application_id: int
    scope: CommentScopeEnum


class CreateCommentRequestSchema(BaseModel):
    application_id: int
    text: str
    scope: CommentScopeEnum
