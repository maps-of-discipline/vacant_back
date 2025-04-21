from fastapi import APIRouter, Body, Depends
from src.logger import get_logger
from src.schemas.comment import CommentSchema, CreateCommentRequestSchema
from src.schemas.status import StatusGetListSchema
from src.services.comment import CommentService
from src.services.status import StatusService

logger = get_logger(__name__)


router = APIRouter(prefix="/comment", tags=["comment"])


@router.post("")
async def get_all_statuses(
    data: CreateCommentRequestSchema = Body(),
    service: CommentService = Depends(),
) -> CommentSchema:
    logger.info("Start handle creating comment")
    comment = await service.create(data)
    logger.info("Stop handle creating comment")
    return comment
