from typing import Any
from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.db import sessionmaker
from src.models.models import Application, User
from src.schemas.user import UserSchema
from src.services.auth import PermissionRequire as Require, PermissionsEnum as p

router = APIRouter(prefix="/test", tags=["sandbox"])


@router.get("/")
async def get_hello_world(
    user: UserSchema = Depends(Require([])),
) -> Any:
    return "await session.scalas"
