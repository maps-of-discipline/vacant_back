from fastapi import Depends
from transliterate import translit


from src.exceptions.general import EntityAlreadyExists, EntityNotFoundException
from src.exceptions.http import (
    EntityAlreadyExistsHTTPException,
    EntityNotFoundHTTPException,
)
from src.gateways.dto import CreateAdminApiUser
from src.models.models import User
from src.repository.user import UserRepository
from src.schemas.user import CreateUserSchema, UserSchema
from src.gateways.admin_api import AdminAPIGateway
from src.settings import settings
from src.logger import get_logger

logger = get_logger(__name__)


class UserService:
    def __init__(
        self,
        user_repository: UserRepository = Depends(),
        admin_api_gateway: AdminAPIGateway = Depends(),
    ):
        self.user_repo = user_repository
        self.admin_gateway = admin_api_gateway

    async def get_by_email(self, email: str) -> UserSchema:
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise EntityNotFoundException("User")
        return user

    async def create_user(self, user: CreateUserSchema) -> UserSchema:
        if await self.user_repo.get_by_email(user.email):
            msg = f"User with email: {user.email} already exists"
            logger.warning(msg)
            raise EntityAlreadyExistsHTTPException(msg)

        admin_api_login = f"{user.name[0]}.{user.patronymic[0]}.{user.surname}"
        admin_api_login: str = translit(admin_api_login, "ru", reversed=True)
        admin_api_login = admin_api_login.lower()

        admin_api_create_user = CreateAdminApiUser(
            name=user.name,
            surname=user.surname,
            patronymic=user.patronymic,
            email=user.email,
            role="student",
            login=admin_api_login,
            faculty=None,
            service_name=settings.admin_api.service_title,
        )

        response = await self.admin_gateway.create_user(admin_api_create_user)

        created_user = await self.user_repo.create_user(
            user=UserSchema(
                id=response.id,
                **user.model_dump(),
            )
        )

        return created_user

    async def update(self, user: UserSchema) -> UserSchema:
        updated_user = await self.user_repo.update(user)
        if not updated_user:
            raise EntityNotFoundHTTPException("User")
        return updated_user
