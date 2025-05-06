from fastapi import BackgroundTasks, Depends

from src.enums.applications import ApplicationStatusEnum
from src.exceptions.http import EntityNotFoundHTTPException
from src.repository.comment import CommentRepository
from src.repository.common_messges import MessagesRepository
from src.schemas.applications.application import (
    ApplicationForListViewSchema,
    ApplicationForStaffListViewSchema,
    CreateQuickComentRequest,
)
from src.repository.applications.application import ApplicationRepository
from src.enums.comment import CommentScopeEnum
from src.schemas.comment import CommentSchema, GetApplicationCommentsRequestSchema
from src.schemas.user import UserSchema
from src.services.file import FileService
from src.services.notificator import NotificationService


class ApplicationService:
    def __init__(
        self,
        tasks: BackgroundTasks,
        repo: ApplicationRepository = Depends(),
        comments_repo: CommentRepository = Depends(),
        message_repo: MessagesRepository = Depends(),
        file_service: FileService = Depends(),
    ) -> None:
        self._repo = repo
        self._comments_repo = comments_repo
        self._message_repo = message_repo
        self._file_service = file_service
        self._background_tasks = tasks

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

        await self._file_service.delete_by_application_id(application_id)
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

    async def quickcomment(
        self, application_id, message_id: int, user: UserSchema
    ) -> CommentSchema:
        application = await self._repo.get(application_id)
        if application is None:
            raise EntityNotFoundHTTPException("Application")

        message = await self._message_repo.get(message_id)
        if message is None:
            raise EntityNotFoundHTTPException("Message")

        comment = await self._comments_repo.add(
            application_id=application.id,
            scope=CommentScopeEnum.user.value,
            user=user,
            text=message.title,
        )

        await self._repo.update_status(application.id, message.status_id)

        notification_service = NotificationService(user, self._background_tasks)
        notification_service.status_changed(application, user)

        return comment

    async def update_status(
        self, application_id: int, status: ApplicationStatusEnum, user: UserSchema
    ) -> None:
        application = await self._repo.get(application_id)
        if not application:
            raise EntityNotFoundHTTPException("Application")

        new_status = await self._repo.update_status(application.id, status)
        application.status = new_status.title
        application.status_verbose_name = new_status.verbose_name

        notification_service = NotificationService(user, self._background_tasks)
        notification_service.status_changed(application, user)
