from typing import Annotated
from fastapi import APIRouter, Body, Depends, Form, Path, UploadFile

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
    application_json: Annotated[str, Form()],
    files: Annotated[list[UploadFile], Form()],
    user: UserSchema = Depends(
        Require(
            [
                p.canCreateSelfApplication,
            ]
        )
    ),
    service: TransferApplicationService = Depends(),
) -> TransferApplicationSchema:
    application = RequestCreateTransferApplicationSchema.model_validate_json(
        application_json
    )
    created_application = await service.create(
        CreateTransferApplicationSchema(**application.model_dump(), user_id=user.id),
        files,
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
    application_json: Annotated[str, Form()],
    files: Annotated[list[UploadFile], Form()],
    _: UserSchema = Depends(
        Require(
            [
                p.canCreateSelfApplication,
            ]
        )
    ),
    service: TransferApplicationService = Depends(),
) -> TransferApplicationSchema:
    application = UpdateTransferApplicationSchema.model_validate_json(application_json)
    logger.info("Start handle update transfer application")
    updated = await service.update(application, files)
    logger.info("Stop handle update transfer application")
    return updated
