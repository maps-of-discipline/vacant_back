import grpc
from typing import Any

from src.settings import settings
from src.logger import get_logger

logger = get_logger(__name__)


class BaseGRPCService:
    stub_class: Any

    def __init__(self):
        self.url = settings.grpc.url
        self._channel: grpc.aio.Channel
        self._stub: Any

    async def __aenter__(self):
        self._channel = grpc.aio.insecure_channel(self.url)
        self._stub = self.stub_class(self._channel)
        return self

    async def __aexit__(self, type, message, traceback):
        await self._channel.close()
