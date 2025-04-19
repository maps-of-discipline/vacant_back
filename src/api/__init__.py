from fastapi.routing import APIRouter
from src.api.applications import router as applications_router
from src.api.users import router as users_router
from src.api.test import router as test_router

router = APIRouter(prefix="/api/v1")

router.include_router(router=applications_router)
router.include_router(router=users_router)
router.include_router(router=test_router)
