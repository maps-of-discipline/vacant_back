from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.models.db import sessionmaker
from src.schemas.applications.application import ApplicationForListViewSchema
from src.schemas.user import UserForListViewSchema
from src.models.models import Application, User


class ApplicationRepository:
    def __init__(self, session: AsyncSession = Depends(sessionmaker)):
        self.session: AsyncSession = session

    async def all(self) -> list[ApplicationForListViewSchema]:
        stmt = (
            select(Application)
            .order_by(Application.id)
            .options(joinedload(Application.user))
        )

        res = await self.session.scalars(stmt)
        applications = []
        for application in res:
            user = UserForListViewSchema(
                id=application.user.id,
                email=application.user.email,
                surname=application.user.surname,
                name=application.user.name,
                patronymic=application.user.patronymic,
                phone=application.user.phone,
                group=application.user.group,
                course=application.user.course,
            )

            applications.append(
                ApplicationForListViewSchema(
                    id=application.id,
                    date=application.date,
                    hostel_policy_accepted=application.hostel_policy_accepted,
                    vacation_policy_viewed=application.vacation_policy_viewed,
                    no_restrictions_policy_accepted=application.no_restrictions_policy_accepted,
                    reliable_information_policy_accepted=application.reliable_information_policy_accepted,
                    user=user,
                )
            )

        return applications
