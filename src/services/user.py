from fastapi import Depends

from src.exceptions.general import EntityNotFoundException
from src.repository.roles import RoleRepository
from src.repository.user import UserRepository
from src.schemas.user import CreateUserSchema, UserSchema


class UserService:
    def __init__(
        self,
        role_repository: RoleRepository = Depends(),
        user_repository: UserRepository = Depends(),
    ):
        self.role_repo = role_repository
        self.user_repo = user_repository

    async def create_new_user(self, user: CreateUserSchema) -> UserSchema:
        roles_for_student = await self.role_repo.get_by_titles(["student"])
        created_user = await self.user_repo.create_user(user, roles=roles_for_student)
        return created_user

    async def get_by_email(self, email: str) -> UserSchema:
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise EntityNotFoundException("User")
        return user
