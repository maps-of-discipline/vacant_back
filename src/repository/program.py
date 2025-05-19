from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from src.models.db import sessionmaker
from src.models.models import Program


class ProgramRepository:
    def __init__(self, session: AsyncSession = Depends(sessionmaker)):
        self.session: AsyncSession = session

    async def get_by_aup(self, aup: str) -> Program | None:
        stmt = select(Program).where(Program.profile == aup)
        program = await self.session.scalar(stmt)
        return program
