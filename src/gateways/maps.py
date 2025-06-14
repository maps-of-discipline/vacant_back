from dataclasses import asdict
import json
import httpx
from src.exceptions.general import BadRequest
from src.gateways.dto.maps import RupData, MapsAupInfo, AllMapsResponse
from src.schemas.rups import GetRupDataSchema
from src.settings import settings
from src.logger import get_logger

logger = get_logger(__name__)


class MapsAPIGateway:
    def __init__(self):
        self.base_url = settings.maps_base_url
        logger.debug(f"init maps gateway with {self.base_url=}")
        self.timeout = 10
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout)

    async def get_rup_data(self, data: GetRupDataSchema) -> RupData:
        logger.debug(f"getting rups data with body: {data.model_dump()}")

        request_data = data.model_dump()
        request_data["aup1"] = request_data.pop("source")
        request_data["aup2"] = request_data.pop("target")
        response = await self.client.post(
            "/rups/get-rups-for-two-aups/v2", json=request_data
        )

        if response.status_code >= 300:
            logger.error(f"{response.status_code} {response.content.decode()}")
            raise BadRequest("Error occured during handling maps http request.")

        return RupData.model_validate(response.json())

    async def get_aup_info(self, aup_num: str) -> MapsAupInfo:
        response = await self.client.get(f"/map/{aup_num}")
        print(response.json()['info'])
        return MapsAupInfo.model_validate(response.json()['info'])

    async def get_all_maps(self) -> AllMapsResponse:
        response = await self.client.get('/getAllMaps')
        return AllMapsResponse.model_validate({"faculties": response.json()})