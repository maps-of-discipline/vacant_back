from sqlalchemy import and_, delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from sqlalchemy.orm import joinedload
from src.gateways.dto.maps import MapsRupDiscipline
from src.models.db import sessionmaker
from src.models.models import Discipline, DisciplineVariant
from src.schemas.discipline import CreateDisciplineSchema, DisciplineSchema


class DisciplineRepository:
    def __init__(self, session: AsyncSession = Depends(sessionmaker)):
        self.session: AsyncSession = session

    async def create(
        self, program_id: int, discipline: CreateDisciplineSchema
    ) -> DisciplineSchema:
        created = Discipline(**discipline.model_dump(), program_id=program_id)
        self.session.add(created)

        return DisciplineSchema(id=created.id, **discipline.model_dump())

    async def get_by_program_id(self, program_id: int) -> list[Discipline]:
        stmt = (
            select(Discipline)
            .where(Discipline.program_id == program_id)
            .options(joinedload(Discipline.variants))
        )
        return list((await self.session.scalars(stmt)).unique())

    async def bukd_save(
        self, program_id: int, disciplines: list[MapsRupDiscipline]
    ) -> list[Discipline]:
        values = []
        for discipline in disciplines:
            value = discipline.model_dump(exclude={"variants", "similarity"})
            value["program_id"] = program_id
            values.append(value)

        __import__("pprint").pprint(values)

        stmt = insert(Discipline).values(values).returning(Discipline)
        return [el[0] for el in await self.session.execute(stmt)]

    async def add_variants(
        self,
        target_discipline: Discipline,
        source_disciplines: dict[str, Discipline],
        variants: list[MapsRupDiscipline],
    ) -> None:
        variant_associations = []
        for variant in variants:
            source_discipline = source_disciplines[variant.title]
            association_object = DisciplineVariant(
                target_id=target_discipline.id,
                variant_id=source_discipline.id,
                similarity=variant.similarity,
                choosen=False,
            )
            variant_associations.append(association_object)

        self.session.add_all(variant_associations)

    async def delete_by_program_id(self, program_id: int) -> None:
        stmt = delete(Discipline).where(Discipline.program_id == program_id)
        await self.session.execute(stmt)

    async def set_choosen(self, target_id: int, variant_id: int, value: bool) -> None:
        stmt = (
            update(DisciplineVariant)
            .where(
                and_(
                    DisciplineVariant.target_id == target_id,
                    DisciplineVariant.variant_id == variant_id,
                )
            )
            .values(choosen=value)
        )

        await self.session.execute(stmt)
