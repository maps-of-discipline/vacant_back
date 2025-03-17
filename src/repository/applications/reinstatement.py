from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


from src.schemas.applications.reinstatement import (
    CreateReinstatementApplicationSchema,
    ReinstatementApplicationSchema,
)
from src.schemas.applications.application import ProgramSchema
from src.models.models import Program, ReinstatementApplication
from src.models.db import sessionmaker


class ReinstatementApplicationRepository:
    def __init__(self, session: AsyncSession = Depends(sessionmaker)):
        self.session: AsyncSession = session

    def _create_schema(
        self, application: ReinstatementApplication
    ) -> ReinstatementApplicationSchema:
        schema = ReinstatementApplicationSchema(
            id=application.id,
            user_id=application.user_id,
            type=application.type,
            status=application.status,
            date=application.date,
            hostel_policy_accepted=application.hostel_policy_accepted,
            vacation_policy_viewed=application.vacation_policy_viewed,
            no_restrictions_policy_accepted=application.vacation_policy_viewed,
            reliable_information_policy_accepted=application.reliable_information_policy_accepted,
            paid_policy_accepted=application.paid_policy_accepted,
            is_vacation_need=application.is_vacation_need,
            begin_year=application.begin_year,
            end_year=application.end_year,
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
        self, application: CreateReinstatementApplicationSchema
    ) -> ReinstatementApplicationSchema:
        application.date = application.date.replace(tzinfo=None)
        created_application = ReinstatementApplication(
            **application.model_dump(exclude={"programs", "type"}),
            status="new",
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

    async def get(self, id: int) -> ReinstatementApplicationSchema | None:
        application = await self.session.get(ReinstatementApplication, id)
        if application is None:
            return None
        return self._create_schema(application)
