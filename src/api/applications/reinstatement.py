from fastapi import APIRouter, Body, Depends, Path

from src.schemas.applications.reinstatement import (
    CreateReinstatementApplicationSchema,
    ReinstatementApplicationSchema,
    RequestCreateReinstatementApplicationSchema,
)

from src.schemas.user import UserSchema
from src.utils.auth import PermissionRequire, PermissionsEnum
from src.services.applications.reinstatement import ReinstatementApplicationService

router = APIRouter(prefix="/reinstatement", tags=["reinstatement"])


@router.post("")
async def create_reinstatement_application(
    user: UserSchema = Depends(
        PermissionRequire(
            [
                PermissionsEnum.canCreateSelfApplication,
            ]
        )
    ),
    application: RequestCreateReinstatementApplicationSchema = Body(),
    service: ReinstatementApplicationService = Depends(),
) -> ReinstatementApplicationSchema:
    created_application = await service.create(
        CreateReinstatementApplicationSchema(
            **application.model_dump(),
            user_id=user.id,
        )
    )
    return created_application


@router.get("/{id}")
async def get_reinstatement_application(
    id: int = Path(), service: ReinstatementApplicationService = Depends()
) -> ReinstatementApplicationSchema:
    application = await service.get(id)
    return application
