import uvicorn
import grpc
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from src.api import router as api_router
from src.settings import settings
from src.services.permissions import PermissionService
from src.logger import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Lifespan: stating initialization...")
        async with PermissionService() as service:
            await service.create_permissions_if_no_exists()
            logger.info("Lifespan: initialization complete.")
    except Exception as e:
        logger.error(f"Lifespan: Error occured during initialization: {e}")
    yield


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
