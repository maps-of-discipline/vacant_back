import uvicorn
from fastapi import FastAPI, Depends

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.db import sessionmaker
from src.models.models import ChangeApplication
from src.api import router as api_router
from src.settings import settings
from src.schemas.applications.change import ChangeApplicationSchema


app = FastAPI()
app.include_router(api_router)


@app.get("/test")
async def test(
    session: AsyncSession = Depends(sessionmaker),
) -> ChangeApplicationSchema:
    stmt = (
        select(ChangeApplication)
        .options(selectinload(ChangeApplication.programs))
        .where(ChangeApplication.id == 4)
    )
    change = await session.scalar(stmt)
    return ChangeApplicationSchema.model_validate(change)


if __name__ == "__main__":
    uvicorn.run(
        app="main:app", host=settings.run.host, port=settings.run.port, reload=True
    )
