from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


from src.schemas.applications.transfer import CreateTransferApplicationSchema
from src.models.models import Program, TransferApplication
from src.models.db import sessionmaker


class TransferApplicationService:
    def __init__(self, session: AsyncSession = Depends(sessionmaker)):
        self.session: AsyncSession = session

    async def create(self, application: CreateTransferApplicationSchema) -> TransferApplication:
        application.date = application.date.replace(tzinfo=None)
        created_application = TransferApplication(
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

