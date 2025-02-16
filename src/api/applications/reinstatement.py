from fastapi import APIRouter, Body, Depends

from src.schemas.applications.reinstatement import (
    CreateReinstatementApplicationSchema,
    ReinstatementApplicationSchema

)
from src.services.applications.reinstatement import ReinstatementApplicationService

router = APIRouter(prefix='/reinstatement')


@router.post("")
async def create_reinstatement_application(
        application: CreateReinstatementApplicationSchema = Body(),
        service: ReinstatementApplicationService = Depends()
) -> str:
    created_application = await service.create(application)
    return "hello world"