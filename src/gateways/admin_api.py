import json
import httpx
from dataclasses import asdict

from src.exceptions.general import BadRequest
from src.exceptions.http import EntityAlreadyExistsHTTPException
from src.gateways.dto import CreateAdminApiUser, CreateAdminApiUserResponse
from src.settings import settings
from src.logger import get_logger

logger = get_logger(__name__)


class AdminAPIGateway:
    def __init__(self, timeout: float = 10.0):
        self.base_url = settings.admin_api.base_url
        self.timeout = timeout
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout)

    async def create_user(self, user: CreateAdminApiUser) -> CreateAdminApiUserResponse:
        logger.debug(asdict(user))
        response = await self.client.post("/api/v1/users/sign-up", json=asdict(user))

        data = response.json()
        if data.get("detail", "") == "user already exists":
            logger.error(f"User with email: {user.email} already exists!")
            raise EntityAlreadyExistsHTTPException(
                f"User with email: {user.email} already exists!"
            )
        if response.status_code >= 300:
            logger.error(f"{response.status_code} {response.json()}")
            raise BadRequest("Error occured during handling admin_adi http response.")

        data = response.json()
        return CreateAdminApiUserResponse(id=data["id"])
