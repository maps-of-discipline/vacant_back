import httpx

from src.settings import settings
from src.logger import logger


class MapsApi:
    def __init__(
        self,
        base_url: str = settings.kd_maps.base_url,
    ):
        logger.info("AdminApi client initialised")
        self.base_url: str = base_url
        self.client: httpx.AsyncClient

    async def __aenter__(
        self,
    ) -> "MapsApi":
        self.client = httpx.AsyncClient(base_url=self.base_url)
        return self

    async def __aexit__(
        self,
        ext_type,
        ext_value,
        traceback,
    ) -> bool | None:
        await self.client.aclose()
        return False if ext_value else None
