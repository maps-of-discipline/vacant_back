import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dataclasses import asdict
import jinja2
import pathlib

from src.utils.notifications.dto import StatusChangedData
from src.utils.notifications.handlers.base import BaseNotificationHandler
from src.settings import settings
from src.logger import get_logger

logger = get_logger(__name__)


class EmailHandler(BaseNotificationHandler):
    def __init__(self) -> None:
        self.host = settings.notifications.email.host
        self.port = settings.notifications.email.port
        self.sender = settings.notifications.email.sender
        self.password = settings.notifications.email.password

        current_dir = pathlib.Path(__file__).parent.absolute()
        templates_dir = current_dir.parent / "templates"

        templateLoader = jinja2.FileSystemLoader(templates_dir)
        templateEnv = jinja2.Environment(loader=templateLoader)
        self.template = templateEnv.get_template(
            "email_application_status_changed_notification.html"
        )

    def status_changed(
        self,
        to: str,
        data: StatusChangedData,
    ) -> None:
        logger.debug("task: start handling email sending")
        try:
            logger.debug(f"email data: {asdict(data)}")
            rendered = self.template.render(asdict(data))
            email_message = MIMEMultipart("alternative")
            email_message["Subject"] = "Изменение статуса заявления"
            email_message["From"] = self.sender
            email_message["To"] = to

            email_message.attach(MIMEText(rendered, "html"))

            server = smtplib.SMTP_SSL(self.host, self.port)
            server.ehlo()
            server.login(self.sender, self.password)
            server.send_message(email_message)
            server.quit()
        except Exception as e:
            logger.error(f"during email sending error occured: {e}")
        finally:
            logger.debug("task: stop handling email sending")
