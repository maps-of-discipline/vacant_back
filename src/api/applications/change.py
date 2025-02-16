from fastapi import APIRouter, Depends, Body

from src.schemas.applications.change import CreateChangeApplicationSchema, ChangeApplicationSchema
from src.services.applications.change import ChangeApplicationService

router = APIRouter(prefix='/change')


@router.post("")
async def create_change_application(
        application: CreateChangeApplicationSchema = Body(),
        transfer_service: ChangeApplicationService = Depends()
) -> str:
    created_application = await transfer_service.create(application)

    return "hello world"
