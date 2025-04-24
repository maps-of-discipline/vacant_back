from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from src.models.db import sessionmaker
from src.models.models import CommonMessages, Status
from src.schemas.status import StatusSchema


class MessagesRepository:
    def __init__(self, session: AsyncSession = Depends(sessionmaker)):
        self.session: AsyncSession = session

    async def get_by_status_id(self, status_id: int) -> list[CommonMessages]:
        res = await self.session.scalars(
            select(CommonMessages).where(CommonMessages.status_id == status_id)
        )
        return list(res)

    async def get(self, id: int) -> CommonMessages | None:
        res = await self.session.scalar(
            select(CommonMessages).where(CommonMessages.id == id)
        )
        return res
