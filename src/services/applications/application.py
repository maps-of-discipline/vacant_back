from fastapi import Depends

from src.exceptions.http import EntityNotFoundHTTPException
from src.repository.comment import CommentRepository
from src.schemas.applications.application import (
    ApplicationForListViewSchema,
    ApplicationForStaffListViewSchema,
)
from src.repository.applications.application import ApplicationRepository
from src.enums.comment import CommentScopeEnum
from src.schemas.comment import CommentSchema, GetApplicationCommentsRequestSchema
from src.schemas.user import UserSchema


class ApplicationService:
    def __init__(
        self,
        repo: ApplicationRepository = Depends(),
        comments_repo: CommentRepository = Depends(),
    ) -> None:
        self._repo = repo
        self._comments_repo = comments_repo

    async def get_users(self, user_id: str) -> list[ApplicationForListViewSchema]:
        applications = await self._repo.all_users(user_id=user_id)
        return applications

    async def all(self) -> list[ApplicationForStaffListViewSchema]:
        applications = await self._repo.all()
        return applications

    async def delete(self, application_id: int) -> ApplicationForListViewSchema:
        application = await self._repo.delete(application_id)
        if not application:
            raise EntityNotFoundHTTPException("Application")

        return application

    async def get_comments(
        self,
        data: GetApplicationCommentsRequestSchema,
        user: UserSchema,
    ) -> list[CommentSchema]:
        application = await self._repo.get(data.application_id)
        if not application:
            raise EntityNotFoundHTTPException("Application")

        comments = await self._comments_repo.get_by_application_id(
            application.id,
            data.scope,
        )
        return [
            CommentSchema(
                id=el.id,
                text=el.text,
                scope=CommentScopeEnum(el.scope),
                by=user.shotname,
            )
            for el in comments
        ]
