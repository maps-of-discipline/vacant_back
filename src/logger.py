import sys
import logging

from src.settings import settings


class LogFormatter(logging.Formatter):
    colors = {
        "DEBUG": "\033[94m",
        "INFO": "\033[92m",
        "WARNING": "\033[93m",
        "ERROR": "\033[91m",
        "CRITICAL": "\033[1m\033[91m",
    }

    def format(self, record) -> str:
        log_color = self.colors.get(record.levelname)
        log_msg = f"{log_color}[{record.levelname:<8}]\033[0m {self.formatTime(record)}: {record.name} - {record.getMessage()}"
        return log_msg


def get_logger(name: str):
    logger = logging.getLogger(name)

    log_level = getattr(logging, settings.logging.level, logging.INFO)
    logger.setLevel(log_level)

    log_format = "[%(levelname)] %(asctime): %(name) - %(message)"

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(LogFormatter())

    # file_handler = logging.FileHandler(settings.logging.log_file)
    # file_handler.setLevel(log_level)
    # file_handler.setFormatter(logging.Formatter(log_format))
    #
    # logger.addHandler(console_handler)
    #
    # if settings.logging.use_file_handler:
    #     logger.addHandler(file_handler)

    return logger
