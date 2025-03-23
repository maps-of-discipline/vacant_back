import random
from typing import Annotated
from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from fastapi import Body, Depends, Header

from src.exceptions.http import NoUserAgenException
from src.schemas.user import AdminApiTokenSchema, CreateUserSchema
from src.schemas.auth import AuthTokens, RenewAccessTokenSchema, SignInSchema
from src.services.user import UserService
from src.services.auth import AuthService

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/login/admin_api")
async def admin_api_login(
    token: Annotated[AdminApiTokenSchema, Body()],
    user_agent: Annotated[str | None, Header()] = None,
    auth_service: AuthService = Depends(),
) -> AuthTokens:
    if not user_agent:
        raise HTTPException(
            status_code=400, detail="User agent header must be in reqeust"
        )

    user = await auth_service.log_in_with_admin_api_token(token)
    tokens = await auth_service.create_user_tokens(user, user_agent)
    return tokens


@router.post("/login/renew")
async def renew_access_token(
    tokens: RenewAccessTokenSchema,
    auth_service: AuthService = Depends(),
    user_agent: Annotated[str | None, Header()] = None,
) -> AuthTokens:
    if not user_agent:
        raise NoUserAgenException()

    return await auth_service.renew_tokens(tokens, user_agent=user_agent)


@router.post("/sign-up")
async def create_new_user(
    user: CreateUserSchema,
    user_agent: Annotated[str | None, Header()] = None,
    user_service: UserService = Depends(),
    auth_service: AuthService = Depends(),
) -> AuthTokens:
    print(user)
    created_user = await user_service.create_new_user(user)
    if not user_agent:
        raise NoUserAgenException()

    tokens = await auth_service.create_user_tokens(created_user, user_agent)
    return tokens


@router.post("/sign-in")
async def log_in_external_user(
    credentials: SignInSchema,
    user_agent: Annotated[str | None, Header()],
    user_service: UserService = Depends(),
    auth_service: AuthService = Depends(),
) -> AuthTokens:
    if not user_agent:
        raise NoUserAgenException()

    user = await user_service.get_by_email(credentials.email)
    return await auth_service.create_user_tokens(user, user_agent)
