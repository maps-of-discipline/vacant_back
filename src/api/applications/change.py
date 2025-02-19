from fastapi import APIRouter, Depends, Body, Path

from src.schemas.applications.change import (
    CreateChangeApplicationSchema,
    ChangeApplicationSchema,
)
from src.services.applications.change import ChangeApplicationService

router = APIRouter(prefix="/change", tags=["change"])


@router.post("")
async def create_change_application(
    application: CreateChangeApplicationSchema = Body(),
    service: ChangeApplicationService = Depends(),
) -> ChangeApplicationSchema:
    created_application = await service.create(application)
    return created_application


@router.get("/{id}")
async def get_change_application(
    id: int = Path(), service: ChangeApplicationService = Depends()
) -> ChangeApplicationSchema:
    application = await service.get(id)
    return application
