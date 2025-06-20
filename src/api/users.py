from fastapi import Body, Depends, status
from fastapi.routing import APIRouter


from src.logger import get_logger
from src.schemas.user import CreateUserSchema, UserSchema
from src.services.user import UserService
from src.services.auth import PermissionRequire as Require
from src.enums import PermissionsEnum as p

logger = get_logger(__name__)


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_external_user(
    user: CreateUserSchema,
    user_service: UserService = Depends(),
) -> None:
    logger.info("Start handle user creation")
    await user_service.create_user(user)
    logger.info("Stop handle user creation")


@router.post("/me")
async def get_user_info(user: UserSchema = Depends(Require([]))) -> UserSchema:
    return user


@router.put("")
async def update_user(
    _: UserSchema = Depends(Require([])),
    update_user: UserSchema = Body(),
    service: UserService = Depends(),
) -> UserSchema:
    logger.info("Start handle update user reuest")
    updated_user = await service.update(update_user)
    logger.info("Stop handle update user reuest")
    return updated_user
