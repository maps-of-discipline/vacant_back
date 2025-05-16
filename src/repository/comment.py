from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from sqlalchemy.orm import joinedload

from src.enums.comment import CommentScopeEnum
from src.models.db import sessionmaker
from src.models.models import Application, Comment
from src.schemas.comment import CommentSchema
from src.schemas.user import UserSchema


class CommentRepository:
    def __init__(self, session: AsyncSession = Depends(sessionmaker)):
        self.session: AsyncSession = session

    async def add(
        self, application_id: int, scope: str, text: str, user: UserSchema
    ) -> CommentSchema:
        comment = Comment(
            application_id=application_id, user_id=user.id, scope=scope, text=text
        )
        self.session.add(comment)
        await self.session.commit()
        await self.session.refresh(comment)
        return CommentSchema(
            id=comment.id,
            text=comment.text,
            scope=CommentScopeEnum(comment.scope),
            by=user.shotname,
            by_id=user.id,
        )

    async def get_by_application_id(
        self, application_id: int, scope: CommentScopeEnum
    ) -> list[Comment]:
        stmt = (
            select(Comment)
            .where(Comment.application_id == application_id, Comment.scope == scope)
            .options(joinedload(Comment.user))
        )
        return list((await self.session.scalars(stmt)).all())

    async def delete(self, id: int) -> int | None:
        stmt = delete(Comment).where(Comment.id == id).returning(Comment.id)
        deleted_id = await self.session.scalar(stmt)
        await self.session.commit()
        return deleted_id

    async def all_related_to_user(self, user_id: str) -> dict[int, list[CommentSchema]]:
        stmt = (
            select(Application.id, Comment)
            .join(Application.comments)
            .where((Application.user_id == user_id) & (Comment.scope == "user"))
            .options(joinedload(Comment.user))
        )
        comments: dict[int, list[CommentSchema]] = {}
        for application_id, comment in await self.session.execute(stmt):
            if application_id not in comments:
                comments.update({application_id: []})

            schema = CommentSchema(
                id=comment.id,
                text=comment.text,
                scope=CommentScopeEnum(comment.scope),
                by=comment.user.shotname,
                by_id=comment.user_id,
            )
            comments[application_id].append(schema)

        return comments
