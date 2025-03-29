# app/dependencies.py
import grpc
from functools import lru_cache
from typing import Dict

from src.settings import settings
from src.grpc.auth import auth_pb2_grpc
from src.grpc.permissions import permissions_pb2_grpc
from src.logger import get_logger

logger = get_logger(__name__)


class GrpcChannelManager:
    """Менеджер gRPC каналов"""

    def __init__(self):
        self.url = settings.grpc.url
        self.channels: Dict[str, grpc.aio.Channel] = {}
        self.stubs = {}

        self._initialize_channels()

    def _initialize_channels(self):
        """Инициализация всех каналов"""
        config = {
            "auth": auth_pb2_grpc.AuthServiceStub,
            "permissions": permissions_pb2_grpc.PermissionServiceStub,
        }

        for title, stub in config.items():
            channel = grpc.aio.insecure_channel(self.url)

            self.channels[title] = channel

            if title == "auth":
                self.stubs[title] = stub(channel)
            elif title == "permissions":
                self.stubs[title] = stub(channel)

    def get_auth_stub(self):
        """Получить стаб для сервиса пользователей"""
        return self.stubs.get("auth")

    def get_permissions_stub(self):
        """Получить стаб для сервиса продуктов"""
        return self.stubs.get("permissions")

    async def close_all_channels(self):
        """Закрыть все каналы при остановке приложения"""
        logger.info("Closing all gRPC channels")
        for title, channel in self.channels.items():
            logger.debug(f"Closing channel: {title}")
            await channel.close()


# Создаем синглтон-менеджер каналов
@lru_cache()
def get_channel_manager():
    return GrpcChannelManager()


# Зависимости для FastAPI
def get_auth_service():
    return get_channel_manager().get_auth_stub()


def get_permissions_service():
    return get_channel_manager().get_permissions_stub()
