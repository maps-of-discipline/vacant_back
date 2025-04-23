from fastapi import Depends
from src.exceptions.http import EntityNotFoundHTTPException
from src.repository.comment import CommentRepository
from src.schemas.comment import CommentSchema, CreateCommentRequestSchema
from src.schemas.user import UserSchema


class CommentService:
    def __init__(
        self,
        comment_repo: CommentRepository = Depends(),
    ):
        self._comment_repo = comment_repo

    async def create(
        self, user: UserSchema, data: CreateCommentRequestSchema
    ) -> CommentSchema:
        comment = await self._comment_repo.add(
            data.application_id,
            data.scope,
            data.text,
            user,
        )
        return comment

    async def delete(self, id: int) -> None:
        res = await self._comment_repo.delete(id)
        if res is None:
            raise EntityNotFoundHTTPException("Comment")

    
