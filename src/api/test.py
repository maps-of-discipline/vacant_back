from fastapi import Depends
from fastapi.routing import APIRouter

from src.schemas.user import UserSchema
from src.services.auth import PermissionRequire as Require, PermissionsEnum as p

router = APIRouter(prefix="/test", tags=["sandbox"])


@router.get("/")
async def get_hello_world(
    user: UserSchema = Depends(
        Require(
            [
                p.canCreateManySelfApplications,
            ]
        )
    ),
) -> str:
    return user.name
