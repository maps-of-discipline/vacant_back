from fastapi import APIRouter, Body, Depends, Path
from src.schemas.comment import CommentSchema, GetApplicationCommentsRequestSchema
from src.schemas.user import UserSchema
from src.services.auth import PermissionRequire as Require, PermissionsEnum as p
from src.schemas.applications.application import (
    ApplicationForListViewSchema,
    ApplicationForStaffListViewSchema,
)
from src.services.applications.application import ApplicationService
from src.logger import get_logger

logger = get_logger(__name__)


router = APIRouter()


@router.get(
    path="/user",
    tags=["application"],
)
async def get_users_applications(
    user: UserSchema = Depends(
        Require(
            [
                p.canViewOwnApplications,
            ]
        )
    ),
    service: ApplicationService = Depends(),
) -> list[ApplicationForListViewSchema]:
    applications = await service.get_users(user_id=user.id)
    return applications


@router.delete(
    path="/{id}",
    tags=["application"],
)
async def delete_application(
    id: int,
    application_service: ApplicationService = Depends(),
) -> ApplicationForListViewSchema:
    application = await application_service.delete(id)
    return application


@router.get(
    path="/comments",
    tags=["application"],
)
async def get_application_comments(
    user: UserSchema = Depends(Require([])),
    data: GetApplicationCommentsRequestSchema = Depends(),
    service: ApplicationService = Depends(),
) -> list[CommentSchema]:
    logger.info("Start handling get application comments")
    comments = await service.get_comments(data, user)
    logger.info("Stop handling get application comments")
    return comments


@router.get("/all", tags=["application"])
async def get_all_applications(
    service: ApplicationService = Depends(),
) -> list[ApplicationForStaffListViewSchema]:
    logger.info("Start handling get all applications")
    applications = await service.all()
    logger.info("Stop handling get all applications")
    return applications
