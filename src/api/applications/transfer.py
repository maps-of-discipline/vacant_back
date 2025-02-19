from fastapi import APIRouter, Body, Depends, Path

from src.schemas.applications.transfer import (
    TransferApplicationSchema,
    CreateTransferApplicationSchema,
)
from src.services.applications.transfer import TransferApplicationService

router = APIRouter(prefix="/transfer", tags=["transfer"])


@router.post("")
async def create_transfer_application(
    application: CreateTransferApplicationSchema = Body(),
    service: TransferApplicationService = Depends(),
) -> TransferApplicationSchema:
    created_application = await service.create(application)
    return created_application


@router.get("/{id}")
async def get_transfer_application(
    id: int = Path(), service: TransferApplicationService = Depends()
) -> TransferApplicationSchema:
    application = await service.get(id)
    return application
