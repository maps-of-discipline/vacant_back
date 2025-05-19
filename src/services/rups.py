from fastapi import Depends
from src.exceptions.general import BadRequest, EntityNotFoundException
from src.gateways.dto.maps import RupData, RupDiscipline
from src.gateways.maps import MapsAPIGateway
from src.models.models import Program
from src.repository.discipline import DisciplineRepository
from src.repository.program import ProgramRepository
from src.schemas.rups import GetRupDataSchema


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

    async def get_rup_data(self, rup_data_request: GetRupDataSchema) -> None:
        source = await self._program_repo.get_by_aup(rup_data_request.source.num)
        target = await self._program_repo.get_by_aup(rup_data_request.target.num)

        if not (source and target):
            raise EntityNotFoundException("One of programs")

        source_disciplines = await self._disc_repo.get_by_program_id(source.id)
        target_disciplines = await self._disc_repo.get_by_program_id(target.id)

        if len(source_disciplines) == 0 or len(target_disciplines) == 0:
            rup_data = await self._save_roop_data(rup_data_request, source, target)
            return rup_data

    async def _save_roop_data(
        self,
        data: GetRupDataSchema,
        source_program: Program,
        target_program: Program,
    ) -> RupData:
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

        return rup_data
