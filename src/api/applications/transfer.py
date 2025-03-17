from fastapi import APIRouter, Body, Depends, Path

from src.schemas.applications.transfer import (
    TransferApplicationSchema,
    CreateTransferApplicationSchema,
    RequestCreateTransferApplicationSchema,
)
from src.schemas.user import UserSchema
from src.services.applications.transfer import TransferApplicationService
from src.utils.auth import PermissionRequire, PermissionsEnum

router = APIRouter(prefix="/transfer", tags=["transfer"])


@router.post("")
async def create_transfer_application(
    user: UserSchema = Depends(
        PermissionRequire(
            [
                PermissionsEnum.canCreateSelfApplication,
            ]
        )
    ),
    application: RequestCreateTransferApplicationSchema = Body(),
    service: TransferApplicationService = Depends(),
) -> TransferApplicationSchema:
    created_application = await service.create(
        CreateTransferApplicationSchema(**application.model_dump(), user_id=user.id)
    )
    return created_application


@router.get("/{id}")
async def get_transfer_application(
    id: int = Path(), service: TransferApplicationService = Depends()
) -> TransferApplicationSchema:
    application = await service.get(id)
    return application
