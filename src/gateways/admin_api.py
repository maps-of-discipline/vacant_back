import json
import httpx
from src.settings import settings
from src.gateways.dto import AdminApiUser, AdminApiServiceRole, AdminApiUserServiceRole
from src.logger import logger


class JWTAuth(httpx.Auth):
    def __init__(self, token):
        self.token = token

    def auth_flow(self, request):
        request.headers["Authorization"] = f"Bearer {self.token}"
        yield request


class AdminApi:
    # TODO: test this shit
    def __init__(
        self,
        token: str,
        base_url: str = settings.admin_api.base_url,
        service_title: str = settings.admin_api.service_title,
    ):
        logger.info("AdminApi client initialised")
        self.base_url: str = base_url
        self.auth: JWTAuth = JWTAuth(token=token)
        self.client: httpx.AsyncClient
        self.service_title = service_title

    async def __aenter__(
        self,
    ) -> "AdminApi":
        self.client = httpx.AsyncClient(base_url=self.base_url, auth=self.auth)
        return self

    async def __aexit__(
        self,
        ext_type,
        ext_value,
        traceback,
    ) -> bool | None:
        await self.client.aclose()
        return False if ext_value else None

    async def fetch_user(self) -> AdminApiUser:
        logger.debug("admin_api client: requesting /api/v1/users/me")
        response = await self.client.get("/api/v1/users/me")
        if response.status_code != 200:
            logger.warning(
                f"admin_api client: response to /api/v1/users/me has status code {response.status_code}"
            )
            raise Exception("/api/v1/users/me with status code", response.status_code)
        return AdminApiUser.from_response(response)

    async def get_vacancy_roles(self) -> list[AdminApiServiceRole]:
        # TODO: impolement pagination

        response = await self.client.post(
            "/api/v1/service-roles/filters",
            json={"service_name": self.service_title},
            params={"page": 1, "size": 20},
        )
        data = response.json()
        roles = []
        for el in data["data"]:
            roles.append(
                AdminApiServiceRole(
                    id=el["id"],
                    service_id=el["service_id"],
                    role=el["role"],
                )
            )

        return roles

    async def get_user_roles(self, user_id: str) -> list[AdminApiUserServiceRole]:
        logger.info(f"getting user({user_id}) roles")

        response = await self.client.post(
            f"/api/v1/users/{user_id}/get_roles_from_service",
            params={"service_name": self.service_title},
        )
        if response.status_code != 200:
            logger.warning(
                f"admin_api response from /api/v1/users/{user_id}/get_roles_from_service has {response.status_code} status code"
            )
        data = response.json()
        logger.debug(
            f"response from /api/v1/users/{user_id}/get_roles_from_service ended wiht data: {data}"
        )
        roles = []
        for role in data["roles"]:
            roles.append(
                AdminApiUserServiceRole(
                    id=role["id"],
                    service_role_id=role["service_roles_id"],
                    user_id=role["user_id"],
                )
            )
        logger.info("user roles has get succesfully")
        return roles
