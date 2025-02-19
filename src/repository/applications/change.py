from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.schemas.applications.change import CreateChangeApplicationSchema
from src.models.models import Program, ChangeApplication
from src.models.db import sessionmaker


class ChangeApplicationService:
    def __init__(self, session: AsyncSession = Depends(sessionmaker)):
        self.session: AsyncSession = session

    async def create(self, application: CreateChangeApplicationSchema) -> ChangeApplication:
        application.date = application.date.replace(tzinfo=None)
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
        return created_application

    async def get(self, id: int) -> ChangeApplication | None:
        return await self.session.get(id)

    async def get_all(self) -> list[ChangeApplication]:
        stmt = select(ChangeApplication).order_by(ChangeApplication.date)
        res = await self.session.scalars(stmt)
        return list(res.all())

    async def filter(self, **filter) -> list[ChangeApplication]:
        stmt = select(ChangeApplication).where(**filter)
        res = await self.session.scalars(stmt)
        return list(res.all())

    async def patch:




