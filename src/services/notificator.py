from fastapi import BackgroundTasks

from src.utils.notifications.handlers.base import BaseNotificationHandler
from src.schemas import UserSchema, ApplicationForListViewSchema
from src.utils.notifications.handlers.email import EmailHandler
from src.utils.notifications.dto import StatusChangedData
from src.logger import get_logger

logger = get_logger(__name__)


class NotificationService:
    def __init__(self, user: UserSchema, background_tasks: BackgroundTasks) -> None:
        logger.info("Initializing notification service")
        self.handlers: list[BaseNotificationHandler] = []
        self.background_tasks = background_tasks

        if user.send_email:
            logger.debug("Added email handler to notification service")
            self.handlers.append(EmailHandler())

    def status_changed(
        self,
        application: ApplicationForListViewSchema,
        user: UserSchema,
    ) -> None:
        appl_type_verbose = {
            "change": "изменение условий обучения",
            "transfer": "перевод из другого вуза",
            "reinstatement": "восстановление",
        }

        data = StatusChangedData(
            user_name=f"{user.surname} {user.name}",
            application_type=appl_type_verbose[application.type],
            status_verbose_name=application.status_verbose_name,
            status=application.status,
        )

        for handler in self.handlers:
            self.background_tasks.add_task(handler.status_changed, user.email, data)
            logger.debug("added notification task")
