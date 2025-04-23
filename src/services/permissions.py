from typing import Awaitable, Callable
from fastapi import Depends, Request

from src.exceptions.auth import PermissionsDeniedException
from src.grpc.dto.permissions import CreatePermission
from src.grpc.permissions_service import PermissionsGRPCService
from src.enums.auth import PermissionsEnum
from src.schemas.user import UserSchema
from src.settings import settings
from src.logger import get_logger


logger = get_logger(__name__)


class PermissionService:
    def __init__(self, permissions_grpc_service: PermissionsGRPCService = Depends()):
        self.permissions_service = permissions_grpc_service
        self.mapper: dict[
            PermissionsEnum, Callable[[UserSchema, Request], Awaitable[bool]]
        ] = {}
        self.settings = settings

    async def create_permissions_if_no_exists(self) -> None:
        logger.info("Permissions syncing on startup application...")
        existing_permissions = await self.permissions_service.get_permissions(
            self.settings.admin_api.service_title
        )

        existing_permissions = {el.title: el for el in existing_permissions}

        logger.debug(
            f"Got existed permissions from admin_api: {list(existing_permissions.keys())}"
        )

        for el in PermissionsEnum:
            if el.value in existing_permissions:
                logger.debug(f"Permission {el.value} already exists in admin_api")
                existing_permissions.pop(el.value)
            else:
                logger.debug(f"Permission {el.value} don't exists in admin_api.")
                await self.permissions_service.create_permission(
                    service_name=self.settings.admin_api.service_title,
                    permission=CreatePermission(title=el.value, verbose_name=""),
                )
                logger.debug(f"Permission {el.value} created.")

        logger.info("Deleting unused permissions...")
        for k, value in existing_permissions.items():
            await self.permissions_service.delete_permission(value.id)
            logger.debug(f"Permission {k} deleted.")
        logger.info("Permissions synched")

    async def check(
        self,
        user: UserSchema,
        user_permissions: list[PermissionsEnum],
        request: Request,
    ):
        for permission in user_permissions:
            if permission in self.mapper and not await self.mapper[permission](
                user, request
            ):
                return False
        return True
