from typing import Any
from fastapi import Depends
from src.exceptions.general import BadRequest, EntityNotFoundException
from src.gateways.maps import MapsAPIGateway
from src.models.models import Program
from src.repository.discipline import DisciplineRepository
from src.repository.program import ProgramRepository
from src.schemas.rups import (
    BestMatchValue,
    ChoosenValueSchema,
    GetRupDataResponseSchema,
    GetRupDataSchema,
    RupDiscipline,
    RupDisciplineVariant,
    RupSameDiscipline,
    SetChoosenRequestSchema,
)


class RupService:
    def __init__(
        self,
        discipline_repo: DisciplineRepository = Depends(),
        maps_gateway: MapsAPIGateway = Depends(),
        program_repository: ProgramRepository = Depends(),
    ):
        self._disc_repo = discipline_repo
        self._maps_api = maps_gateway
        self._program_repo = program_repository

    async def get_rup_data(
        self, rup_data_request: GetRupDataSchema
    ) -> GetRupDataResponseSchema:
        source = await self._program_repo.get_by_aup(rup_data_request.source.num)
        target = await self._program_repo.get_by_aup(rup_data_request.target.num)

        if not (source and target):
            raise EntityNotFoundException("One of programs")

        source_disciplines = {
            el.title: el for el in await self._disc_repo.get_by_program_id(source.id)
        }
        target_disciplines = {
            el.title: el for el in await self._disc_repo.get_by_program_id(target.id)
        }

        if len(source_disciplines) == 0 or len(target_disciplines) == 0:
            if len(source_disciplines) != 0:
                await self._disc_repo.delete_by_program_id(source.id)
            if len(target_disciplines) != 0:
                await self._disc_repo.delete_by_program_id(target.id)

            await self._save_roop_data(rup_data_request, source, target)

            source_disciplines = {
                el.title: el
                for el in await self._disc_repo.get_by_program_id(source.id)
            }
            target_disciplines = {
                el.title: el
                for el in await self._disc_repo.get_by_program_id(target.id)
            }

        same = []
        for title, discipline in [*target_disciplines.items()]:
            if title in source_disciplines:
                same.append(discipline)
                source_disciplines.pop(title)
                target_disciplines.pop(title)

        similar: list[RupSameDiscipline] = []
        best_match: dict[str, BestMatchValue] = {}
        choosen: dict[str, ChoosenValueSchema] = {}

        for title, discipline in target_disciplines.items():
            if not discipline.variants:
                continue

            similar_item = RupSameDiscipline.from_model(discipline)
            similar.append(similar_item)

            choosen_variants: dict[str, bool] = {}
            for variant in discipline.variants:
                best_variant = best_match.get(
                    variant.variant.title, BestMatchValue(target="", similarity=0)
                )
                choosen_variants.update({variant.variant.title: bool(variant.choosen)})
                if variant.similarity > best_variant.similarity:
                    best_match.update(
                        {
                            variant.variant.title: BestMatchValue(
                                target=title,
                                similarity=variant.similarity,
                            )
                        }
                    )

            choosen.update(
                {
                    title: ChoosenValueSchema(
                        period=discipline.period, variants=choosen_variants
                    )
                }
            )

        source_disciplines = [
            RupDiscipline.from_model(el) for el in source_disciplines.values()
        ]
        target_disciplines = [
            RupDiscipline.from_model(el) for el in target_disciplines.values()
        ]
        same = [RupDiscipline.from_model(el) for el in same]
        return GetRupDataResponseSchema(
            source=source_disciplines,
            target=target_disciplines,
            same=same,
            similar=similar,
            best_match=best_match,
            choosen=choosen,
        )

    async def _save_roop_data(
        self,
        data: GetRupDataSchema,
        source_program: Program,
        target_program: Program,
    ) -> None:
        rup_data = await self._maps_api.get_rup_data(data)
        maps_source_disciplines = [
            *rup_data.same,
            *rup_data.source,
        ]

        maps_target_disciplines = [
            *rup_data.same,
            *rup_data.target,
        ]

        source_disciplines = await self._disc_repo.bukd_save(
            source_program.id, maps_source_disciplines
        )
        target_disciplines = await self._disc_repo.bukd_save(
            target_program.id, maps_target_disciplines
        )
        print(target_disciplines)
        source_disciplines = {el.title: el for el in source_disciplines}
        target_disciplines = {el.title: el for el in target_disciplines}

        for discipline in rup_data.similar:
            target = target_disciplines[discipline.title]
            await self._disc_repo.add_variants(
                target,
                source_disciplines,
                discipline.variants,
            )

    async def set_choosen(self, data: SetChoosenRequestSchema) -> None:
        await self._disc_repo.set_choosen(
            target_id=data.target_id, variant_id=data.variant_id, value=data.value
        )
