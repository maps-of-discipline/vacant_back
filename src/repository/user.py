from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.exceptions.general import EntityNotFoundError
from src.models.db import sessionmaker
from src.models.models import Role, User, Permission
from src.schemas.auth import PermissionSchema
from src.schemas.user import UserSchema
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
            passport_data=user.passport_data,
            phone=user.phone,
            course=user.course,
            group=user.group,
            snils=user.snils,
        )

    async def get(self, id: int) -> UserSchema | None:
        stmt = select(User).where(User.id == id)
        user = await self.session.scalar(stmt)
        if user:
            return self._create_schema(user)
        else:
            return None

    async def get_by_external_id(self, external_id: str) -> UserSchema | None:
        print(external_id)
        stmt = select(User).where(User.external_id == external_id)
        user = await self.session.scalar(stmt)
        print(f"{user=}")
        if user:
            return self._create_schema(user)
        else:
            return None

    async def create_from_admin_api(self, user: AdminApiUser) -> UserSchema:
        created_user = User(
            email=user.email,
            external_id=user.id,
            name=user.name,
            surname=user.surname,
            patronymic=user.patronymic,
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
        user = await self.session.scalar(select(User).where(User.id == user_id).options(joinedload(User.roles)))
        if user is None:
            logger.warning(f"User with id {user_id} hasn't been found")
            raise EntityNotFoundError("User")

        role_ids = [el.service_role_id for el in roles]

        stmt = select(Role).where(Role.external_id.in_(role_ids))
        user_roles = await self.session.scalars(stmt)
        user.roles = list(user_roles)

        self.session.add(user)
        await self.session.commit()

