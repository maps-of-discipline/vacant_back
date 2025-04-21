from fastapi import Depends
from src.repository.comment import CommentRepository
from src.schemas.comment import CommentSchema, CreateCommentRequestSchema


class CommentService:
    def __init__(
        self,
        comment_repo: CommentRepository = Depends(),
    ):
        self._comment_repo = comment_repo

    async def create(self, data: CreateCommentRequestSchema) -> CommentSchema:
        comment = await self._comment_repo.add(
            data.application_id, data.scope, data.text
        )
        return comment
