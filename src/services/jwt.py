import jwt
from src.settings import settings
from src.schemas.auth import JWTPayload
from time import time
from src.exceptions.auth import TokenExpiredException


class JWTService:
    def __init__(
        self,
    ):
        self.access_lifetime = settings.auth.access_token_lifetime
        self.secret = settings.auth.secret
        self.algorithm = settings.auth.algorithm

    def encode(
        self,
        payload: JWTPayload,
    ) -> str:
        token_payload = {
            **payload.model_dump(),
            "iat": int(time()),
            "exp": int(time() + self.access_lifetime),
        }
        return jwt.encode(
            token_payload,
            key=self.secret,
            algorithm=self.algorithm,
        )

    def decode(self, token: str) -> JWTPayload:
        try:
            payload = jwt.decode(
                token,
                key=self.secret,
                algorithms=[self.algorithm],
                options={
                    "verify_exp": True,
                },
            )
        except jwt.ExpiredSignatureError:
            raise TokenExpiredException()

        return JWTPayload.model_validate(payload)
