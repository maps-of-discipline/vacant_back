from fastapi import FastAPI
from settings import settings
import uvicorn


app = FastAPI()


if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host=settings.run.host,
        port=settings.run.port,
    )
