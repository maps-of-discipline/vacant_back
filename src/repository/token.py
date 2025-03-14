from time import time
from fastapi import Depends
from sqlalchemy import delete, and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from secrets import token_urlsafe

from src.exceptions.auth import InvalidTokenException
from src.models.models import Token
from src.models.db import sessionmaker


class TokenRepository:
    def __init__(
        self,
        session: AsyncSession = Depends(sessionmaker),
    ):
        self.session = session

    async def remove_unused_tokens(self, user_id: int, user_agent: str) -> None:
        stmt = delete(Token).where(
            and_(
                Token.user_id == user_id,
                or_(Token.user_agent == user_agent, Token.exp <= time()),
            )
        )
        await self.session.execute(stmt)

    async def create_refresh_token(
        self,
        user_id: int,
        user_agent: str,
        lifetime: int,
    ) -> str:
        await self.remove_unused_tokens(user_id, user_agent)
        token = token_urlsafe(64)
        self.session.add(
            Token(
                user_id=user_id,
                user_agent=user_agent,
                token=token,
                exp=int(time() + lifetime),
            )
        )
        await self.session.commit()
        return token

    async def renew_token(
        self,
        refrest_token: str,
        user_id: int,
        user_agent: str,
        lifetime: int,
    ) -> str:
        stmt = select(Token).where(
            Token.user_id == user_id,
            Token.user_agent == user_agent,
            Token.token == refrest_token,
        )

        token = await self.session.scalar(stmt)
        if not token:
            raise InvalidTokenException("Invalid refrest token")

        return await self.create_refresh_token(user_id, user_agent, lifetime)
