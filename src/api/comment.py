from fastapi import APIRouter, Body, Depends, Path
from src.logger import get_logger
from src.schemas.comment import CommentSchema, CreateCommentRequestSchema
from src.schemas.user import UserSchema
from src.services.comment import CommentService
from src.services.auth import PermissionRequire as Require
from src.enums import PermissionsEnum as p

logger = get_logger(__name__)


router = APIRouter(prefix="/comment", tags=["comment"])


@router.delete("/{id}")
async def get_all_statuses(
    id: int = Path(),
    service: CommentService = Depends(),
) -> None:
    logger.info("Start handle creating comment")
    await service.delete(id)
    logger.info("Stop handle creating comment")


@router.post("/")
async def create_comment(
    user: UserSchema = Depends(Require([])),
    data: CreateCommentRequestSchema = Body(),
    service: CommentService = Depends(),
) -> CommentSchema:
    logger.info("Start comment creation request handling")
    new_comment = await service.create(user, data)
    logger.info("Stop comment creation request handling")
    return new_comment


@router.get("/users")
async def get_users_comments(
    user: UserSchema = Depends(Require([])),
    service: CommentService = Depends(),
) -> dict[int, list[CommentSchema]]:
    logger.info("Start get users comments request handling")
    comments = await service.get_all_by_user(user.id)
    logger.info("Stop get users comments request handling")
    return comments
