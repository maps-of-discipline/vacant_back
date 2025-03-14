from fastapi import Depends
from fastapi.routing import APIRouter

from src.schemas.user import UserSchema
from src.utils.auth import PermissionRequire, PermissionsEnum

router = APIRouter(prefix="/test", tags=["sandbox"])


@router.get("/")
async def get_hello_world(
    user: UserSchema = Depends(
        PermissionRequire(
            [
                # PermissionsEnum.penrm1,
                # PermissionsEnum.perm2,
            ]
        )
    ),
) -> str:
    return user.name
