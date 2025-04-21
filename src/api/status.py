from fastapi import APIRouter, Depends
from src.logger import get_logger
from src.schemas.status import StatusGetListSchema
from src.services.status import StatusService

logger = get_logger(__name__)


router = APIRouter(prefix="/status", tags=["status"])


@router.get("/all")
async def get_all_statuses(
    service: StatusService = Depends(),
) -> list[StatusGetListSchema]:
    logger.info("Start handle get status list")
    res = await service.get_all()
    logger.info("Stop handle get status list")
    return res
