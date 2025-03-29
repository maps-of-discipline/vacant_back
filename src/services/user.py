from fastapi import Depends

from src.exceptions.general import EntityNotFoundException
from src.repository.user import UserRepository
from src.schemas.user import UserSchema


class UserService:
    def __init__(
        self,
        user_repository: UserRepository = Depends(),
    ):
        self.user_repo = user_repository

    async def get_by_email(self, email: str) -> UserSchema:
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise EntityNotFoundException("User")
        return user
