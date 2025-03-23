import random
import uuid

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload


from src.exceptions.general import EntityAlreadyExists, EntityNotFoundException
from src.models.db import sessionmaker
from src.models.models import Role, User, Permission
from src.schemas.auth import PermissionSchema
from src.schemas.user import UserSchema, CreateUserSchema
from src.gateways.dto import AdminApiUserServiceRole
from src.gateways.dto import AdminApiUser
from src.logger import logger


class UserRepository:
    def __init__(self, session: AsyncSession = Depends(sessionmaker)):
        self.session: AsyncSession = session

    @staticmethod
    def _create_schema(user: User) -> UserSchema:
        return UserSchema(
            id=user.id,
            external_id=user.external_id,
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

    async def get(self, id: int) -> UserSchema | None:
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

    async def get_by_external_id(self, external_id: str) -> UserSchema | None:
        stmt = select(User).where(User.external_id == external_id)
        user = await self.session.scalar(stmt)
        if user:
            return self._create_schema(user)
        else:
            return None

    async def create_user(
        self,
        user: CreateUserSchema,
        roles: list[Role] | None,
    ) -> UserSchema:
        stmt = select(User).where(User.email == user.email)
        if await self.session.scalar(stmt):
            raise EntityAlreadyExists("User")

        user.birtdate = user.birtdate.replace(tzinfo=None)
        user.passport_issued_date = user.passport_issued_date.replace(tzinfo=None)

        created_user = User(**user.model_dump(), external_id=str(uuid.uuid4()))
        if roles:
            created_user.roles = roles

        self.session.add(created_user)
        await self.session.commit()
        await self.session.refresh(created_user)
        return self._create_schema(created_user)

    async def create_from_admin_api(self, user: AdminApiUser) -> UserSchema:
        created_user = User(
            **CreateUserSchema(
                course=None,
                phone=None,
                snils=None,
                email=user.email,
                name=user.name,
                surname=user.surname,
                patronymic=user.patronymic,
            ).model_dump(),
            external_id=user.id,
        )

        self.session.add(created_user)
        await self.session.commit()
        await self.session.refresh(created_user)
        return self._create_schema(created_user)

    async def assign_admin_api_roles_if_no_exists(
        self,
        user_id: int,
        roles: list[AdminApiUserServiceRole],
    ) -> None:
        logger.info("UserRepo: assignind roles")
        user = await self.session.scalar(
            select(User).where(User.id == user_id).options(joinedload(User.roles))
        )
        if user is None:
            logger.warning(f"User with id {user_id} hasn't been found")
            raise EntityNotFoundException("User")

        role_ids = [el.service_role_id for el in roles]

        stmt = select(Role).where(Role.external_id.in_(role_ids))
        user_roles = await self.session.scalars(stmt)
        user.roles = list(user_roles)

        self.session.add(user)
        await self.session.commit()
