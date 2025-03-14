from pydantic import BaseModel


class AuthTokens(BaseModel):
    access_token: str
    refresh_token: str


class PermissionSchema(BaseModel):
    id: int
    title: str


class JWTPayload(BaseModel):
    user_id: int
    permissions: list[PermissionSchema]

    class Config:
        extra = "allow"
