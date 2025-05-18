from fastapi import APIRouter, Body, Depends
from src.gateways.dto.maps import RupData
from src.logger import get_logger
from src.schemas.rups import GetRupDataSchema
from src.schemas.status import StatusGetListSchema
from src.services.rups import RupService

logger = get_logger(__name__)


router = APIRouter(prefix="/rups", tags=["rups"])


@router.post("/get")
async def get_all_statuses(
    service: RupService = Depends(),
    data: GetRupDataSchema = Body(),
) -> RupData:
    logger.info("Start handle get status list")
    res = await service.get_rup_data(data)
    logger.info("Stop handle get status list")
    return res
