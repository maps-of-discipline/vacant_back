from fastapi.routing import APIRouter

from src.api.applications.transfer import router as transfer_router
from src.api.applications.reinstatement import router as reinstatement_router
from src.api.applications.change import router as change_router
from src.api.applications.application import router as application_router

router = APIRouter(prefix="/applications")

router.include_router(transfer_router)
router.include_router(reinstatement_router)
router.include_router(change_router)
router.include_router(application_router)
