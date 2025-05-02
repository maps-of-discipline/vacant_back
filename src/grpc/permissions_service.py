import grpc
from grpc.aio import AioRpcError

from src.exceptions.grpc import ServiceNotFoundException
from src.grpc.permissions import permissions_pb2, permissions_pb2_grpc
from src.grpc.dto import Permission, CreatePermission
from src.logger import get_logger
from src.grpc.grpc_manager import BaseGRPCService

logger = get_logger(__name__)


class PermissionsGRPCService(BaseGRPCService):
    stub_class = permissions_pb2_grpc.PermissionServiceStub

    async def get_permissions(self, service_name: str) -> list[Permission]:
        try:
            request = permissions_pb2.GetPermissionsByServiceRequest(
                service_name=service_name
            )
            response = await self._stub.GetPermissionsByService(request)
            return [
                Permission(
                    id=el.id,
                    title=el.title,
                    verbose_name=el.verbose_name,
                )
                for el in response.permissions
            ]
        except AioRpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                logger.error("gRPC Error: Service not found")
                raise ServiceNotFoundException()
            logger.error(f"gRPC Error: {e}")
            raise

    async def create_permission(
        self, service_name: str, permission: CreatePermission
    ) -> Permission:
        logger.debug(f"Creating permission: {permission.title}")
        create_permission = permissions_pb2.CreatePermission(
            title=permission.title, verbose_name=permission.verbose_name or ""
        )
        request = permissions_pb2.CreateServicePermissionRequest(
            service_name=service_name, permission=create_permission
        )
        try:
            response = await self._stub.CreateServicePermission(request)
            permission = response.permission
            return Permission(
                id=permission.id,
                title=permission.title,
                verbose_name=permission.verbose_name,
            )
        except AioRpcError as e:
            logger.error(f"gRPC Error occurred during creating permission: {e}")
            raise

    async def update_permission(
        self, service_name: str, permission: Permission
    ) -> None:
        update_permission = permissions_pb2.Permission(
            id=permission.id,
            title=permission.title,
            verbose_name=permission.verbose_name or "",
        )
        request = permissions_pb2.UpdateServicePermissionRequest(
            service_name=service_name, permission=update_permission
        )
        await self._stub.UpdateServicePermission(request)

    async def delete_permission(self, permission_id: str) -> None:
        request = permissions_pb2.DeleteServicePermissionRequest(id=permission_id)
        await self._stub.DeleteServicePermission(request)
