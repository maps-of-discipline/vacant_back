import uvicorn
from fastapi import FastAPI

from src.api import router as api_router
from src.settings import settings



app = FastAPI()
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True
    )
