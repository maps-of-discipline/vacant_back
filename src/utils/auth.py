from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.schemas.user import UserSchema
from src.services.auth import AuthService
from src.services.jwt import JWTService
from src.repository.user import UserRepository
from src.exceptions.auth import InvalidTokenException, PermissionsDeniedException
from src.enums.auth import PermissionsEnum
from src.logger import logger


class PermissionRequire:
    def __init__(self, permissions: list[PermissionsEnum]):
        self.required: list[PermissionsEnum] = permissions

    async def __call__(
        self,
        token: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
        user_repo: UserRepository = Depends(),
        auth_service: AuthService = Depends(),
        jwt_service: JWTService = Depends(),
    ) -> UserSchema:
        logger.info("Checking user permissions before request")
        payload = jwt_service.decode(
            token.credentials, options={"verify_exp": True, "verify_signature": True}
        )

        logger.debug(f"Users's {payload=}")
        user = await user_repo.get(payload.user_id)
        logger.debug(f"Routes required permissions: {self.required}")
        if not user:
            raise InvalidTokenException("User not found.")
        if not (
            self.required == []
            or await auth_service.veryfi_permissions(user, self.required)
        ):
            raise PermissionsDeniedException()
        return user
