from typing import Annotated

from fastapi import Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import grpc

from src.schemas.user import UserSchema
from src.repository.user import UserRepository
from src.exceptions import InvalidTokenException, PermissionsDeniedException, BadRequest
from src.enums.auth import PermissionsEnum
from src.grpc import AuthGRPCService
from src.grpc.dto import TokenPayload
from src.services.permissions import PermissionService
from src.logger import get_logger


logger = get_logger(__name__)


class PermissionRequire:
    def __init__(self, permissions: list[PermissionsEnum]):
        self.required: list[PermissionsEnum] = permissions
        self._user_repo: UserRepository
        self._permissions_service: PermissionService

    async def __call__(
        self,
        token: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
        request: Request,
        user_repo: UserRepository = Depends(),
        auth_grpc_service: AuthGRPCService = Depends(),
        permissions_service: PermissionService = Depends(),
    ) -> UserSchema:
        logger.info("Checking user permissions before request")
        self._user_repo = user_repo
        self._auth_service = auth_grpc_service
        self._permissions_service = permissions_service
        async with self._auth_service, self._permissions_service:
            try:
                payload: TokenPayload = await self._auth_service.get_payload(
                    jwt_token=token.credentials
                )

            except grpc.aio.AioRpcError as e:
                s = grpc.StatusCode
                if e.code() in [s.UNAUTHENTICATED, s.PERMISSION_DENIED]:
                    logger.error(
                        f"gRPC response have status: {e.code()}: {e.details()}"
                    )
                    raise InvalidTokenException(e.details())
                else:
                    logger.error(f"GRPC error with status: {e.code()}: {e.details()}")
                    raise BadRequest(str(e.details()))

            user = await self._user_repo.get(payload.user_id)

            if not user:
                logger.info("User not found, creating new one.")
                user = await self._create_user(token.credentials)

            if any(perm.value not in payload.permissions for perm in self.required):
                logger.info("User does not have required permissions.")
                raise PermissionsDeniedException()

            if not await self._permissions_service.check(
                user,
                [PermissionsEnum(el) for el in payload.permissions],
                request,
            ):  # type: ignore
                logger.info("User doesn't pass permissions check")
                raise PermissionsDeniedException()
        logger.info("Permissions validated")
        return user  # type: ignore

    async def _create_user(self, token: str) -> UserSchema:
        admin_api_user = await self._auth_service.get_user_data(jwt_token=token)
        user = await self._user_repo.create_user(
            UserSchema(
                id=admin_api_user.id,
                email=admin_api_user.email,
                name=admin_api_user.name,
                surname=admin_api_user.surname,
                patronymic=admin_api_user.patronymic,
                phone=None,
                course=None,
                snils=None,
            )
        )
        return user
