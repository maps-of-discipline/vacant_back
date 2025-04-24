from fastapi import APIRouter, Body, Depends, Path

from src.schemas.applications.transfer import (
    TransferApplicationSchema,
    CreateTransferApplicationSchema,
    RequestCreateTransferApplicationSchema,
    UpdateTransferApplicationSchema,
)
from src.schemas.user import UserSchema
from src.services.applications.transfer import TransferApplicationService
from src.services.auth import PermissionRequire as Require, PermissionsEnum as p
from src.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/transfer", tags=["transfer"])


@router.post("")
async def create_transfer_application(
    user: UserSchema = Depends(
        Require(
            [
                p.canCreateSelfApplication,
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


@router.put("")
async def update_application(
    data: UpdateTransferApplicationSchema = Body(),
    service: TransferApplicationService = Depends(),
) -> TransferApplicationSchema:
    logger.info("Start handle update transfer application")
    updated = await service.update(data)
    logger.info("Stop handle update transfer application")
    return updated
