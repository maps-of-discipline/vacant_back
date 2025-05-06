from abc import ABC, abstractmethod

from src.utils.notifications.dto import StatusChangedData


class BaseNotificationHandler(ABC):
    @abstractmethod
    def status_changed(
        self,
        to: str,
        data: StatusChangedData,
    ) -> None: ...
