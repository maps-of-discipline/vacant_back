from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.models.db import sessionmaker
from src.models.models import User, Role
from src.gateways.dto import AdminApiServiceRole
from src.schemas.roles import RoleSchema


class RoleRepository:
    def __init__(self, session: AsyncSession = Depends(sessionmaker)):
        self.session = session

    async def create_from_admin_api(self, role: AdminApiServiceRole) -> RoleSchema:
        created_role: Role = Role(title=role.role, external_id=role.id)
        self.session.add(created_role)
        await self.session.commit()
        await self.session.refresh(created_role)

        return RoleSchema(
            id=created_role.id,
            title=created_role.title,
            external_id=created_role.external_id,
        )

    async def all(self) -> list[RoleSchema]:
        stmt = select(Role)
        roles = await self.session.scalars(stmt)
        return [
            RoleSchema(id=el.id, title=el.title, external_id=el.external_id)
            for el in roles
        ]

    async def get_by_user_id(self, user_id: int) -> list[RoleSchema]:
        stmt = (
            select(Role)
            .join(Role.users)
            .where(User.id == user_id)
            .options(joinedload(Role.users))
        )

        roles = await self.session.scalars(stmt)
        return [
            RoleSchema(id=el.id, title=el.title, external_id=el.external_id)
            for el in roles
        ]

    async def get_by_titles(self, titles: list[str]) -> list[Role]:
        stmt = select(Role).where(Role.title.in_(titles))
        roles = await self.session.scalars(stmt)
        return list(roles)
