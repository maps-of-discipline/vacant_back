from __future__ import annotations

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.enums.applications import ApplicationStatusEnum as StatusEnum
from src.schemas.applications.application import ProgramSchema
from src.schemas.applications.change import (
    ChangeApplicationSchema,
    CreateChangeApplicationSchema,
    UpdateChangeApplicationChema,
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
            status=StatusEnum(application.status.title),
            date=application.date,
            hostel_policy_accepted=application.hostel_policy_accepted,
            vacation_policy_viewed=application.vacation_policy_viewed,
            no_restrictions_policy_accepted=application.vacation_policy_viewed,
            reliable_information_policy_accepted=application.reliable_information_policy_accepted,
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
        self, application: CreateChangeApplicationSchema, status_id: int
    ) -> ChangeApplicationSchema:
        application.date = application.date.replace(tzinfo=None)
        created_application = ChangeApplication(
            **application.model_dump(exclude={"programs", "type", "status"}),
            status_id=status_id,
        )

        self.session.add(created_application)

        created_programs = []
        for program in application.programs:
            program = Program(**program.model_dump())
            created_programs.append(program)

            self.session.add(program)

        created_application.programs = created_programs
        await self.session.commit()
        await self.session.refresh(created_application, ["status"])
        return self._create_schema(created_application)

    async def get(self, id: int) -> ChangeApplicationSchema | None:
        stmt = (
            select(ChangeApplication)
            .where(ChangeApplication.id == id)
            .options(joinedload(ChangeApplication.status))
        )
        application = await self.session.scalar(stmt)
        return None if application is None else self._create_schema(application)

    async def update(
        self,
        data: UpdateChangeApplicationChema,
        status_id: int,
    ) -> ChangeApplicationSchema | None:
        stmt = (
            select(ChangeApplication)
            .where(ChangeApplication.id == data.id)
            .options(
                joinedload(ChangeApplication.programs),
                joinedload(ChangeApplication.status),
            )
        )

        application = await self.session.scalar(stmt)

        if application is None:
            return None

        for key, value in data.model_dump(
            exclude={"programs", "id", "status", "type"}
        ).items():
            setattr(application, key, value)

        application.status_id = status_id
        self.session.add(application)

        programs = {el.id: el for el in data.programs}
        for i, program in enumerate(application.programs):
            for key, value in programs[program.id].model_dump(exclude={"id"}).items():
                setattr(application.programs[i], key, value)

            self.session.add(application.programs[i])
        await self.session.commit()

        return self._create_schema(application)
