from fastapi import Depends
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.exceptions.http import EntityNotFoundHTTPException
from src.models.db import sessionmaker
from src.schemas.applications.application import (
    ApplicationForListViewSchema,
    ApplicationForStaffListViewSchema,
)
from src.schemas.status import StatusSchema
from src.models.models import Application, Status, User
from src.enums.applications import ApplicationStatusEnum


class ApplicationRepository:
    def __init__(self, session: AsyncSession = Depends(sessionmaker)):
        self.session: AsyncSession = session

    async def all_users(self, user_id: str) -> list[ApplicationForListViewSchema]:
        stmt = (
            select(Application)
            .join(User.applications)
            .order_by(Application.id)
            .where(User.id == user_id)
            .options(joinedload(Application.user))
            .options(joinedload(Application.status))
        )

        res = await self.session.scalars(stmt)
        applications = []
        for application in res:
            applications.append(
                ApplicationForListViewSchema(
                    id=application.id,
                    date=application.date,
                    type=application.type,
                    status=ApplicationStatusEnum(application.status.title),
                    status_verbose_name=application.status.verbose_name,
                    hostel_policy_accepted=application.hostel_policy_accepted,
                    vacation_policy_viewed=application.vacation_policy_viewed,
                    no_restrictions_policy_accepted=application.no_restrictions_policy_accepted,
                    reliable_information_policy_accepted=application.reliable_information_policy_accepted,
                )
            )

        return applications

    async def delete(self, id: int) -> ApplicationForListViewSchema | None:
        stmt = (
            select(Application)
            .where(Application.id == id)
            .options(joinedload(Application.status))
        )

        application = await self.session.scalar(stmt)
        if not application:
            return None

        stmt = delete(Application).where(Application.id == id)
        await self.session.execute(stmt)
        await self.session.commit()

        return ApplicationForListViewSchema(
            id=application.id,
            date=application.date,
            type=application.type,
            status=ApplicationStatusEnum(application.status.title),
            status_verbose_name=application.status.verbose_name,
            hostel_policy_accepted=application.hostel_policy_accepted,
            vacation_policy_viewed=application.vacation_policy_viewed,
            no_restrictions_policy_accepted=application.no_restrictions_policy_accepted,
            reliable_information_policy_accepted=application.reliable_information_policy_accepted,
        )

    async def get(self, id: int) -> ApplicationForListViewSchema | None:
        application = await self.session.scalar(
            select(Application)
            .where(Application.id == id)
            .options(joinedload(Application.status))
        )
        if not application:
            return None

        return ApplicationForListViewSchema(
            id=application.id,
            date=application.date,
            type=application.type,
            status=ApplicationStatusEnum(application.status.title),
            status_verbose_name=application.status.verbose_name,
            hostel_policy_accepted=application.hostel_policy_accepted,
            vacation_policy_viewed=application.vacation_policy_viewed,
            no_restrictions_policy_accepted=application.no_restrictions_policy_accepted,
            reliable_information_policy_accepted=application.reliable_information_policy_accepted,
        )

    async def all(self) -> list[ApplicationForStaffListViewSchema]:
        stmt = (
            select(Application)
            .join(User.applications)
            .order_by(Application.id)
            .options(joinedload(Application.user))
            .options(joinedload(Application.status))
        )

        res = await self.session.scalars(stmt)
        applications = []

        for application in res:
            applications.append(
                ApplicationForStaffListViewSchema(
                    id=application.id,
                    date=application.date,
                    fio=application.user.fullname,
                    type=application.type,
                    status=ApplicationStatusEnum(application.status.title),
                    status_verbose_name=application.status.verbose_name,
                    hostel_policy_accepted=application.hostel_policy_accepted,
                    vacation_policy_viewed=application.vacation_policy_viewed,
                    no_restrictions_policy_accepted=application.no_restrictions_policy_accepted,
                    reliable_information_policy_accepted=application.reliable_information_policy_accepted,
                )
            )

        return applications

    async def update_status(
        self, id: int, status: ApplicationStatusEnum | int
    ) -> StatusSchema:
        stmt = select(Status)

        if isinstance(status, ApplicationStatusEnum):
            stmt = stmt.where(Status.title == status.value)
        elif isinstance(status, int):
            stmt = stmt.where(Status.id == status)

        status_ = await self.session.scalar(stmt)
        if not status_:
            raise EntityNotFoundHTTPException("Status")

        stmt = (
            update(Application).where(Application.id == id).values(status_id=status_.id)
        )
        await self.session.execute(stmt)

        return StatusSchema(
            id=status_.id, title=status_.title, verbose_name=status_.verbose_name
        )


    async def get_raw(self, application_id: int) -> Application:
        return await self.session.scalar(select(Application).where(Application.id == application_id))
