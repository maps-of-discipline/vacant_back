from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from src.enums.comment import CommentScopeEnum
from src.models.db import sessionmaker
from src.models.models import Comment
from src.schemas.comment import CommentSchema


class CommentRepository:
    def __init__(self, session: AsyncSession = Depends(sessionmaker)):
        self.session: AsyncSession = session

    async def add(self, application_id: int, scope: str, text: str) -> CommentSchema:
        comment = Comment(application_id=application_id, scope=scope, text=text)
        self.session.add(comment)
        await self.session.commit()
        await self.session.refresh(comment)
        return CommentSchema(id=comment.id, text=comment.text)

    async def get_by_application_id(
        self, application_id: int, scope: CommentScopeEnum
    ) -> list[CommentSchema]:
        stmt = select(Comment).where(
            Comment.application_id == application_id, Comment.scope == scope
        )
        comments = await self.session.scalars(stmt)
        return [CommentSchema(id=el.id, text=el.text) for el in comments]
