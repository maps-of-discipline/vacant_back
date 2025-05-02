from typing import Annotated
from fastapi import APIRouter, Depends, Body, Form, Path, UploadFile

from src.schemas.applications.change import (
    CreateChangeApplicationSchema,
    RequestCreateChangeApplicationSchema,
    ChangeApplicationSchema,
    UpdateChangeApplicationChema,
)
from src.schemas.user import UserSchema
from src.services.applications.change import ChangeApplicationService
from src.services.auth import PermissionRequire as Require, PermissionsEnum as p
from src.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/change", tags=["change"])


@router.post("")
async def create_change_application(
    application_json: Annotated[str, Form()],
    files: Annotated[list[UploadFile], Form()],
    service: ChangeApplicationService = Depends(),
    user: UserSchema = Depends(
        Require(
            [
                p.canCreateSelfApplication,
            ]
        )
    ),
) -> ChangeApplicationSchema:
    application = RequestCreateChangeApplicationSchema.model_validate_json(
        application_json
    )
    application_wiht_user_id = CreateChangeApplicationSchema(
        user_id=user.id, **application.model_dump()
    )
    created_application = await service.create(application_wiht_user_id, files)

    return created_application


@router.get("/{id}")
async def get_change_application(
    id: int = Path(), service: ChangeApplicationService = Depends()
) -> ChangeApplicationSchema:
    application = await service.get(id)
    return application


@router.put("")
async def update_application(
    application_json: Annotated[str, Form()],
    files: Annotated[list[UploadFile], Form()],
    service: ChangeApplicationService = Depends(),
    _: UserSchema = Depends(
        Require(
            [
                p.canCreateSelfApplication,
            ]
        )
    ),
) -> ChangeApplicationSchema:
    application = UpdateChangeApplicationChema.model_validate_json(application_json)
    logger.info("Start handle update chagne application")
    updated = await service.update(application, files)
    logger.info("Stop handle update chagne application")
    return updated
