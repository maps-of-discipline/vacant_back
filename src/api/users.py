import random
from typing import Annotated
from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from fastapi import Body, Depends, Header

from src.exceptions.http import NoUserAgentException
from src.schemas.user import AdminApiTokenSchema
from src.services.user import UserService

router = APIRouter(prefix="/users", tags=["users"])


# @router.post("/sign-up")
# async def create_new_user(
#     user: CreateUserSchema,
#     user_agent: Annotated[str | None, Header()] = None,
#     user_service: UserService = Depends(),
#     auth_service: AuthService = Depends(),
# ) -> AuthTokens:
#     created_user = await user_service.create_new_user(user)
#     if not user_agent:
#         raise NoUserAgentException()

#     tokens = await auth_service.create_user_tokens(created_user, user_agent)
#     return tokens


# @router.post("/sign-in")
# async def log_in_external_user(
#     credentials: SignInSchema,
#     user_agent: Annotated[str | None, Header()],
#     user_service: UserService = Depends(),
#     auth_service: AuthService = Depends(),
# ) -> AuthTokens:
#     if not user_agent:
#         raise NoUserAgentException()
#
#     user = await user_service.get_by_email(credentials.email)
#     return await auth_service.create_user_tokens(user, user_agent)
