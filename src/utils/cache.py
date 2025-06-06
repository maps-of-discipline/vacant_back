from dataclasses import dataclass
from typing import Any, Callable
import time
from functools import wraps
from src.logger import get_logger

logger = get_logger(__name__)


@dataclass
class CachedValue:
    expires_at: int
    value: Any


class TTLCache:
    def __init__(self, ttl: int = 60):
        self._cache: dict[str, CachedValue] = {}
        self._ttl = ttl
        self.getter: Callable[[str, tuple, dict], str] | None = None

    def __getitem__(self, key: str) -> Any | None:
        if key in self._cache:
            if self._cache[key].expires_at > time.time():
                return self._cache[key].value
            del self._cache[key]
        return None

    def __setitem__(self, key: str, value: Any) -> None:
        self._cache[key] = CachedValue(
            expires_at=int(time.time() + self._ttl),
            value=value,
        )

    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = (
                self.getter(func.__name__, args, kwargs)
                if self.getter
                else func.__name__
            )
            logger.debug(f"use {key} key for caching")
            if cached := self[key]:
                logger.debug(f"Using cached result for {func.__name__}")
                return cached

            logger.debug(f"No cached value found for func {func.__name__}.")

            result = await func(*args, **kwargs)
            self[key] = result
            return result

        return wrapper

    def key(self, key_func: Callable[[str, tuple, dict], str]) -> Callable:
        self.getter = key_func
        return self.__call__
