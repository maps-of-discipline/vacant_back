from fastapi import Depends
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.models.db import sessionmaker
from src.schemas.applications.application import ApplicationForListViewSchema
from src.schemas.user import UserForListViewSchema
from src.models.models import Application, User
from src.enums.applications import ApplicationStatusEnum


class ApplicationRepository:
    def __init__(self, session: AsyncSession = Depends(sessionmaker)):
        self.session: AsyncSession = session

    async def all(self, user_id: str) -> list[ApplicationForListViewSchema]:
        stmt = (
            select(Application)
            .join(User.applications)
            .order_by(Application.id)
            .where(User.id == user_id)
            .options(joinedload(Application.user))
        )

        res = await self.session.scalars(stmt)
        applications = []
        for application in res:
            applications.append(
                ApplicationForListViewSchema(
                    id=application.id,
                    date=application.date,
                    type=application.type,
                    status=ApplicationStatusEnum(application.status),
                    hostel_policy_accepted=application.hostel_policy_accepted,
                    vacation_policy_viewed=application.vacation_policy_viewed,
                    no_restrictions_policy_accepted=application.no_restrictions_policy_accepted,
                    reliable_information_policy_accepted=application.reliable_information_policy_accepted,
                )
            )

        return applications

    async def delete(self, id: int) -> ApplicationForListViewSchema | None:
        stmt = delete(Application).where(Application.id == id).returning(Application)
        application = await self.session.scalar(stmt)
        if not application:
            return None

        return ApplicationForListViewSchema(
            id=application.id,
            date=application.date,
            type=application.type,
            status=ApplicationStatusEnum(application.status),
            hostel_policy_accepted=application.hostel_policy_accepted,
            vacation_policy_viewed=application.vacation_policy_viewed,
            no_restrictions_policy_accepted=application.no_restrictions_policy_accepted,
            reliable_information_policy_accepted=application.reliable_information_policy_accepted,
        )

    async def get(self, id: int) -> ApplicationForListViewSchema | None:
        application = await self.session.scalar(
            select(Application).where(Application.id == id)
        )
        if not application:
            return None

        return ApplicationForListViewSchema(
            id=application.id,
            date=application.date,
            type=application.type,
            status=ApplicationStatusEnum(application.status),
            hostel_policy_accepted=application.hostel_policy_accepted,
            vacation_policy_viewed=application.vacation_policy_viewed,
            no_restrictions_policy_accepted=application.no_restrictions_policy_accepted,
            reliable_information_policy_accepted=application.reliable_information_policy_accepted,
        )
