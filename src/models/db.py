from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, declared_attr
import re
from src.settings import settings

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
    AsyncSession,
)


engine: AsyncEngine = create_async_engine(
    url=str(settings.db.url),
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
)

session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    autoflush=settings.db.autoflush,
    autocommit=settings.db.autocommit,
    expire_on_commit=settings.db.expire_on_commit,
)


async def sessionmaker():
    """Provide a transactional scope around a series of operations."""
    session = session_factory()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


class BaseModel(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__camel_to_snake(cls.__name__)

    @classmethod
    def __camel_to_snake(cls, camel: str) -> str:
        snake_str = re.sub("([a-z0-9])([A-Z])", r"\1_\2", camel).lower()
        return snake_str
