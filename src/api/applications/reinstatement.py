from fastapi import APIRouter, Body, Depends, Path

from src.schemas.applications.reinstatement import (
    CreateReinstatementApplicationSchema,
    ReinstatementApplicationSchema,
)
from src.services.applications.reinstatement import ReinstatementApplicationService

router = APIRouter(prefix="/reinstatement", tags=["reinstatement"])


@router.post("")
async def create_reinstatement_application(
    application: CreateReinstatementApplicationSchema = Body(),
    service: ReinstatementApplicationService = Depends(),
) -> ReinstatementApplicationSchema:
    created_application = await service.create(application)
    return created_application


@router.get("/{id}")
async def get_reinstatement_application(
    id: int = Path(), service: ReinstatementApplicationService = Depends()
) -> ReinstatementApplicationSchema:
    application = await service.get(id)
    return application
