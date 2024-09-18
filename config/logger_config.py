import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logging():
    # Ensure the logs directory exists
    log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
    os.makedirs(log_dir, exist_ok=True)

    # Path for the log file
    log_file_path = os.path.join(log_dir, "telegram_bot.log")

    logger = logging.getLogger("TelegramBotLogger")
    logger.setLevel(logging.INFO)

    # Configure file handler
    handler = RotatingFileHandler(log_file_path, maxBytes=5000000, backupCount=5)
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)

    return logger


# Initialize the logger
logger = setup_logging()
