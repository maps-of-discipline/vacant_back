from fastapi import Depends
from src.gateways.dto.maps import RupData
from src.gateways.maps import MapsAPIGateway
from src.repository.discipline import DisciplineRepository
from src.schemas.rups import GetRupDataSchema


class RupService:
    def __init__(
        self,
        discipline_repo: DisciplineRepository = Depends(),
        maps_gateway: MapsAPIGateway = Depends(),
    ):
        self._disc_repo = discipline_repo
        self._maps_api = maps_gateway

    async def get_rup_data(self, rup_data_request: GetRupDataSchema) -> RupData:
        rup_data = await self._maps_api.get_rup_data(rup_data_request)
        return rup_data
