import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter

from src.applications import router as applications_router
from src.settings import settings

api_router = APIRouter(
    prefix="/api/v1"
)
api_router.include_router(router=applications_router)


app = FastAPI()
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True
    )
