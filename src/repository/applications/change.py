from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.applications.application import ProgramSchema
from src.schemas.applications.change import (
    ChangeApplicationSchema,
    CreateChangeApplicationSchema,
)
from src.models.models import Program, ChangeApplication
from src.models.db import sessionmaker


class ChangeApplicationRepository:
    def __init__(self, session: AsyncSession = Depends(sessionmaker)):
        self.session: AsyncSession = session

    def _create_schema(self, application: ChangeApplication) -> ChangeApplicationSchema:
        schema = ChangeApplicationSchema(
            id=application.id,
            user_id=application.user_id,
            type=application.type,
            date=application.date,
            hostel_policy_accepted=application.hostel_policy_accepted,
            vacation_policy_viewed=application.vacation_policy_viewed,
            no_restrictions_policy_accepted=application.vacation_policy_viewed,
            reliable_information_policy_accepted=application.reliable_information_policy_accepted,
            change_date=application.change_date.replace(tzinfo=None),
            purpose=application.purpose,
            programs=[],
        )

        programs = []
        for program in application.programs:
            programs.append(
                ProgramSchema(
                    id=program.id,
                    type=program.type,
                    application_id=program.application_id,
                    priority=program.priority,
                    okso=program.okso,
                    profile=program.profile,
                    form=program.form,
                    base=program.base,
                    sem_num=program.sem_num,
                    university=program.university,
                )
            )

        schema.programs = programs
        return schema

    async def create(
        self, application: CreateChangeApplicationSchema
    ) -> ChangeApplicationSchema:
        application.date = application.date.replace(tzinfo=None)
        application.change_date = application.change_date.replace(tzinfo=None)
        created_application = ChangeApplication(
            **application.model_dump(exclude={"programs", "type"})
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
        return self._create_schema(created_application)

    async def get(self, id: int) -> ChangeApplicationSchema | None:
        application = await self.session.get(ChangeApplication, id)
        return None if application is None else self._create_schema(application)
