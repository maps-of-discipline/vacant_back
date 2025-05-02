from src.grpc.dto.auth import UserData

from src.grpc.auth import auth_pb2_grpc, auth_pb2
from src.grpc.grpc_servcie import BaseGRPCService
from src.grpc.dto import TokenPayload
from src.logger import get_logger


logger = get_logger(__name__)


class AuthGRPCService(BaseGRPCService):
    stub_class = auth_pb2_grpc.AuthServiceStub

    async def get_payload(self, jwt_token: str) -> TokenPayload:
        logger.debug("GRPC: Getting payload from auth service")
        request = auth_pb2.GetPayloadRequest(token=jwt_token)
        response = await self._stub.GetPayload(request)

        payload = TokenPayload(
            user_id=response.user_id,
            role=response.role,
            expires_at=response.expires_at,
            service_name=response.service_name,
            permissions=response.permissions,
        )
        return payload

    async def get_user_data(self, jwt_token: str) -> UserData:
        request = auth_pb2.GetUserRequest(token=jwt_token)
        response = await self._stub.GetUser(request)
        return UserData(
            id=response.id,
            external_id=response.external_id,
            role=response.role,
            external_role=response.external_role,
            name=response.name,
            surname=response.surname,
            patronymic=response.patronymic,
            email=response.email,
            faculty=response.faculty,
            login=response.login,
            last_login=response.last_login,
            created_at=response.created_at,
        )
