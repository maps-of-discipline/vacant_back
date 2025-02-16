from fastapi import APIRouter, Body, Depends

from src.schemas.applications.transfer import CreateTransferApplicationSchema
from src.services.applications.transfer import TransferApplicationService

router = APIRouter(prefix='/transfer')


@router.post("")
async def create_transfer_application(
        application: CreateTransferApplicationSchema = Body(),
        service: TransferApplicationService = Depends()
):
    created_application = await service.create(application)
    return 'Hello world'