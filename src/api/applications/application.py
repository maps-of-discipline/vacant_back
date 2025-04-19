from fastapi import APIRouter, Depends
from src.schemas.user import UserSchema
from src.services.auth import PermissionRequire as Require, PermissionsEnum as p
from src.schemas.applications.application import ApplicationForListViewSchema
from src.services.applications.application import ApplicationService

router = APIRouter(prefix="/applications")


@router.get(
    path="",
    tags=["application"],
)
async def get_all_applications(
    user: UserSchema = Depends(
        Require(
            [
                p.canViewOwnApplications,
            ]
        )
    ),
    service: ApplicationService = Depends(),
) -> list[ApplicationForListViewSchema]:
    applications = await service.get_all(user_id=user.id)
    return applications
