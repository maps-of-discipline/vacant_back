from fastapi import Depends

from src.exceptions.auth import InvalidTokenException
from src.schemas.auth import AuthTokens, JWTPayload, RenewAccessTokenSchema
from src.schemas.user import AdminApiTokenSchema, UserSchema
from src.gateways.admin_api import AdminApi

from src.repository.user import UserRepository
from src.repository.permission import PermissionRepository
from src.repository.roles import RoleRepository
from src.repository.token import TokenRepository
from src.services.jwt import JWTService
from src.enums.auth import PermissionsEnum
from src.settings import settings
from src.logger import logger


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository = Depends(),
        roles_repository: RoleRepository = Depends(),
        permission_repository: PermissionRepository = Depends(),
        token_repository: TokenRepository = Depends(),
        jwt_service: JWTService = Depends(),
    ):
        self.user_repo = user_repository
        self.role_repo = roles_repository
        self.permission_repo = permission_repository
        self.token_repo = token_repository
        self.jwt = jwt_service
        self.refresh_lifetime = settings.auth.refresh_token_lifetime

    async def log_in_with_admin_api_token(
        self, token: AdminApiTokenSchema
    ) -> UserSchema:
        async with AdminApi(token.token) as client:
            logger.debug("AuthService: logging whith admin-api token")
            vacancy_roles = await client.get_vacancy_roles()
            logger.info(f"AuthService: got vacancy roles: {vacancy_roles}")
            existing_roles = [el.title for el in await self.role_repo.all()]

            for role in vacancy_roles:
                if role.role not in existing_roles:
                    await self.role_repo.create_from_admin_api(role)

            logger.info("AuthService: added unexisted roles")
            admin_api_user = await client.fetch_user()
            logger.info(f"AuthService: user {admin_api_user.id} has fetched")

            user: UserSchema | None = await self.user_repo.get_by_external_id(
                admin_api_user.id
            )

            if not user:
                logger.info(
                    f"AuthService: user {admin_api_user} hasn't finded in db. Adding new one."
                )
                user = await self.user_repo.create_from_admin_api(admin_api_user)
            admin_api_user_roles = await client.get_user_roles(admin_api_user.id)
            await self.user_repo.assign_admin_api_roles_if_no_exists(
                user.id, admin_api_user_roles
            )
            return user

    async def veryfi_permissions(
        self,
        user: UserSchema,
        has_have: list[PermissionsEnum],
    ) -> bool:
        logger.info("veryfing permissions...")
        permissions = await self.permission_repo.get_user_permissions(user.id)

        has_have_set = set([el.value for el in has_have])
        permissions_set = set([el.title for el in permissions])
        res = has_have_set.issubset(permissions_set)

        logger.info("veryfing " + ("successd" if res else "failed"))
        if not res:
            logger.debug(
                f"user has have permissions: {has_have_set} \nbut have: {permissions_set}"
            )

        return res

    async def create_user_tokens(self, user: UserSchema, user_agent: str) -> AuthTokens:
        permissions = await self.permission_repo.get_user_permissions(user_id=user.id)

        payload = JWTPayload(user_id=user.id, permissions=permissions)
        access_token = self.jwt.encode(payload)

        refresh_token = await self.token_repo.create_refresh_token(
            user.id, user_agent=user_agent, lifetime=self.refresh_lifetime
        )

        return AuthTokens(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def renew_tokens(
        self,
        tokens: RenewAccessTokenSchema,
        user_agent: str,
    ) -> AuthTokens:
        payload = self.jwt.decode(
            tokens.access_token, options={"verify_signature": True}
        )

        user = await self.user_repo.get(payload.user_id)

        if not user:
            raise InvalidTokenException("User not found.")
        permissions = await self.permission_repo.get_user_permissions(user_id=user.id)

        payload = JWTPayload(user_id=user.id, permissions=permissions)
        access = self.jwt.encode(payload)

        refresh = await self.token_repo.renew_token(
            tokens.refresh_token,
            user.id,
            user_agent,
            self.refresh_lifetime,
        )

        return AuthTokens(access_token=access, refresh_token=refresh)
