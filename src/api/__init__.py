from fastapi.routing import APIRouter
from src.api.applications import router as applications_router

router = APIRouter(
    prefix="/api/v1"
)

router.include_router(router=applications_router)
