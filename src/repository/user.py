import random
import uuid

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exists, select
from sqlalchemy.orm import joinedload


from src.exceptions.general import EntityAlreadyExists, EntityNotFoundException
from src.models.db import sessionmaker
from src.models.models import User
from src.schemas.user import UserSchema
from src.gateways.dto import AdminApiUserServiceRole
from src.gateways.dto import AdminApiUser
from src.logger import get_logger

logger = get_logger(__name__)


class UserRepository:
    def __init__(self, session: AsyncSession = Depends(sessionmaker)):
        self.session: AsyncSession = session

    @staticmethod
    def _create_schema(user: User) -> UserSchema:
        return UserSchema(
            id=user.id,
            email=user.email,
            name=user.name,
            surname=user.surname,
            patronymic=user.patronymic,
            phone=user.phone,
            course=user.course,
            group=user.group,
            snils=user.snils,
            sex=user.sex,
            birtdate=user.birtdate,
            passport_series=user.passport_series,
            passport_birthplace=user.passport_birthplace,
            passport_issued_by=user.passport_issued_by,
            passport_issued_code=user.passport_issued_code,
            passport_issued_date=user.passport_issued_date,
        )

    async def get(self, id: str) -> UserSchema | None:
        stmt = select(User).where(User.id == id)
        user = await self.session.scalar(stmt)
        if user:
            return self._create_schema(user)
        else:
            return None

    async def get_by_email(self, email: str) -> UserSchema | None:
        stmt = select(User).where(User.email == email)
        user = await self.session.scalar(stmt)
        return self._create_schema(user) if user else None

    async def create_user(
        self,
        user: UserSchema,
    ) -> UserSchema:
        stmt = select(User).where(User.email == user.email)
        if await self.session.scalar(stmt):
            raise EntityAlreadyExists("User")

        user.birtdate = user.birtdate.replace(tzinfo=None)
        user.passport_issued_date = user.passport_issued_date.replace(tzinfo=None)

        created_user = User(**user.model_dump())

        self.session.add(created_user)
        await self.session.commit()
        await self.session.refresh(created_user)
        return self._create_schema(created_user)
