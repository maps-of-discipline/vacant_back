from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.applications.change import CreateChangeApplicationSchema
from src.models.models import Program, ChangeApplication
from src.models.db import sessionmaker


class ChangeApplicationService:
    def __init__(self, session: AsyncSession = Depends(sessionmaker)):
        self.session: AsyncSession = session

    async def create(self, application: CreateChangeApplicationSchema) -> ChangeApplication:
        created_application = ChangeApplication(
            date=application.date.replace(tzinfo=None),
            user_id=1,
            hostel_policy_accepted=application.hostel_policy_accepted,
            vacation_policy_viewed=application.vacation_policy_viewed,
            no_restrictions_policy_accepted=application.no_restrictions_policy_accepted,
            reliable_information_policy_accepted=application.reliable_information_policy_accepted,
            change_date=application.change_date.replace(tzinfo=None),
            purpose=application.purpose,
        )

        self.session.add(created_application)

        created_programs = []
        for program in application.programs:
            program = Program(**program.model_dump())
            created_programs.append(program)

            self.session.add(program)

        created_application.programs = created_programs
        await self.session.commit()
        await self.session.refresh(created_application)
        return created_application


