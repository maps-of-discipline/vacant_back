import json
import httpx
from src.settings import settings
from src.gateways.dto import AdminApiUser, AdminApiServiceRole, AdminApiUserServiceRole


class JWTAuth(httpx.Auth):
    def __init__(self, token):
        self.token = token

    def auth_flow(self, request):
        request.headers["Authentication"] = self.token
        yield request


class AdminApi:
    # TODO: test this shit
    def __init__(
        self,
        token: str,
        base_url: str = settings.admin_api.base_url,
        service_title: str = settings.admin_api.service_title,
    ):
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
        user = await self.client.get("/api/v1/users/me")
        return AdminApiUser.from_response(user)

    async def get_vacancy_roles(self) -> list[AdminApiServiceRole]:
        # TODO: impolement pagination

        response = await self.client.post(
            "/api/v1/service-roles/filters",
            data={"service_name": self.service_title},
            params={"page": 1, "size": 20},
        )

        data = json.loads(response.json())
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
        response = await self.client.post(
            f"/api/v1/users/{user_id}/get_roles_from_service",
            params={"service_name": self.service_title},
        )
        data = json.loads(response.json())
        roles = []
        for role in data["roles"]:
            roles.append(
                AdminApiUserServiceRole(
                    id=role["id"],
                    service_role_id=role["service_role_id"],
                    user_id=role["user_id"],
                )
            )
        return roles
