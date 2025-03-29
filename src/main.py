import uvicorn
import grpc
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from src.api import router as api_router
from src.settings import settings
from src.services.permissions import PermissionService
from src.grpc.permissions_service import PermissionsGRPCService
from src.grpc.grpc_manager import get_channel_manager, get_permissions_service
from src.logger import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Lifespan: stating initialization...")
        stub = get_permissions_service()
        grpc_service = PermissionsGRPCService(stub)
        service = PermissionService(grpc_service)
        await service.create_permissions_if_no_exists()
        logger.info("Lifespan: initialization complete.")
    except Exception as e:
        logger.error(f"Lifespan: Error occured during initialization: {e}")
    yield
    manager = get_channel_manager()
    await manager.close_all_channels()


app = FastAPI(
    lifespan=lifespan,
)
app.include_router(api_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.api.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
