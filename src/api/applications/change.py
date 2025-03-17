from fastapi import APIRouter, Depends, Body, Path

from src.schemas.applications.change import (
    CreateChangeApplicationSchema,
    RequestCreateChangeApplicationSchema,
    ChangeApplicationSchema,
)
from src.schemas.user import UserSchema
from src.services.applications.change import ChangeApplicationService
from src.utils.auth import PermissionRequire, PermissionsEnum

router = APIRouter(prefix="/change", tags=["change"])


@router.post("")
async def create_change_application(
    user: UserSchema = Depends(
        PermissionRequire([PermissionsEnum.canCreateSelfApplication])
    ),
    application: RequestCreateChangeApplicationSchema = Body(),
    service: ChangeApplicationService = Depends(),
) -> ChangeApplicationSchema:
    application_wiht_user_id = CreateChangeApplicationSchema(
        user_id=user.id, **application.model_dump()
    )
    created_application = await service.create(application_wiht_user_id)
    return created_application


@router.get("/{id}")
async def get_change_application(
    id: int = Path(), service: ChangeApplicationService = Depends()
) -> ChangeApplicationSchema:
    application = await service.get(id)
    return application
