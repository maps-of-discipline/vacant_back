from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from src.models.db import sessionmaker
from src.models.models import Discipline
from src.schemas.discipline import CreateDisciplineSchema, DisciplineSchema


class DisciplineRepository:
    def __init__(self, session: AsyncSession = Depends(sessionmaker)):
        self.session: AsyncSession = session

    async def create(
        self, program_id: int, discipline: CreateDisciplineSchema
    ) -> DisciplineSchema:
        created = Discipline(**discipline.model_dump())
        self.session.add(created)

        return DisciplineSchema(id=created.id, **discipline.model_dump())
