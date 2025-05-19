from fastapi import APIRouter, Body, Depends
from src.gateways.dto.maps import RupData
from src.logger import get_logger
from src.schemas.rups import GetRupDataSchema, SetChoosenRequestSchema
from src.schemas.status import StatusGetListSchema
from src.services.rups import RupService

logger = get_logger(__name__)


router = APIRouter(prefix="/rups", tags=["rups"])


@router.post("/get")
async def get_all_statuses(
    service: RupService = Depends(),
    data: GetRupDataSchema = Body(),
):
    logger.info("Start handle get status list")
    res = await service.get_rup_data(data)
    logger.info("Stop handle get status list")
    return res


@router.post("/set-choosen")
async def set_choosen(
    service: RupService = Depends(),
    data: SetChoosenRequestSchema = Body(),
) -> None:
    logger.info("Start handle set_choosen request")
    await service.set_choosen(data)
    logger.info("Stop handle set_choosen request")
