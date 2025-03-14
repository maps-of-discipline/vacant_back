from typing import Annotated
from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from fastapi import Body, Depends, Header

from src.schemas.user import AdminApiTokenSchema
from src.services.auth import AuthService
from src.schemas.auth import AuthTokens, RenewAccessTokenSchema

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
        raise HTTPException(
            status_code=400, detail="User agent header must be in reqeust"
        )
    return await auth_service.renew_tokens(tokens, user_agent=user_agent)
