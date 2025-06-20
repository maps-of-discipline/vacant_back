from fastapi.routing import APIRouter
from src.api.applications import router as applications_router
from src.api.users import router as users_router
from src.api.test import router as test_router
from src.api.status import router as status_router
from src.api.comment import router as comment_router
from src.api.files import router as files_router
from src.api.rups import router as rups_router
from src.api.documents import router as documents_router

router = APIRouter(prefix="/api/v1")

router.include_router(router=applications_router)
router.include_router(router=users_router)
router.include_router(router=test_router)
router.include_router(router=status_router)
router.include_router(router=comment_router)
router.include_router(router=files_router)
router.include_router(router=rups_router)
router.include_router(router=documents_router)
