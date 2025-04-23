from fastapi import APIRouter, Body, Depends, Path

from src.schemas.applications.reinstatement import (
    CreateReinstatementApplicationSchema,
    ReinstatementApplicationSchema,
    RequestCreateReinstatementApplicationSchema,
    UpdateReinstatementApplicationSchema,
)

from src.schemas.user import UserSchema
from src.services.auth import PermissionRequire as Require, PermissionsEnum as p
from src.services.applications.reinstatement import ReinstatementApplicationService
from src.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/reinstatement", tags=["reinstatement"])


@router.post("")
async def create_reinstatement_application(
    user: UserSchema = Depends(
        Require(
            [
                p.canCreateSelfApplication,
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


@router.put("/")
async def update_application(
    data: UpdateReinstatementApplicationSchema = Body(),
    service: ReinstatementApplicationService = Depends(),
) -> ReinstatementApplicationSchema:
    logger.info("Start handle update reinstatement application")
    updated = await service.update(data)
    logger.info("Stop handle update reinstatement application")
    return updated
