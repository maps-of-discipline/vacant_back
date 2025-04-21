from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from src.models.db import sessionmaker
from src.models.models import Status
from src.schemas.status import StatusSchema


class StatusRepository:
    def __init__(self, session: AsyncSession = Depends(sessionmaker)):
        self.session: AsyncSession = session

    async def create(self, title: str, verbose: str) -> StatusSchema:
        status = Status(title=title, verbose_name=verbose)
        self.session.add(status)

        await self.session.commit()
        await self.session.refresh(status)
        return StatusSchema(
            id=status.id, title=status.title, verbose_name=status.verbose_name
        )

    async def get_by_title(self, title: str) -> StatusSchema | None:
        status = await self.session.scalar(select(Status).where(Status.title == title))

        if not status:
            return None

        return StatusSchema(
            id=status.id, title=status.title, verbose_name=status.verbose_name
        )

    async def get_all(self):
        stmt = select(Status)
        return await self.session.scalars(stmt)
