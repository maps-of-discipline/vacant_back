from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import aliased
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.db import sessionmaker
from src.models.models import User, Role, Permission
from src.schemas.auth import PermissionSchema


class PermissionRepository:
    def __init__(
        self,
        session: AsyncSession = Depends(sessionmaker),
    ):
        self.session = session

    async def get_user_permissions(self, user_id: int) -> list[PermissionSchema]:
        role_alias = aliased(Role)
        permission_alias = aliased(Permission)

        stmt = (
            select(permission_alias)
            .join(role_alias.permissions)  # Join through the alias for permissions
            .join(User.roles)  # Join user with roles
            .filter(User.id == user_id)
            .distinct()
        )
        permissions = await self.session.scalars(stmt)
        return [PermissionSchema(id=el.id, title=el.title) for el in permissions]
