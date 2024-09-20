import logging
import sys


def setup_logging():
    # Configure logger
    logger = logging.getLogger("TelegramBotLogger")
    logger.setLevel(logging.INFO)

    # Configure stream handler to output logs to stdout
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    handler.setFormatter(formatter)

    # Attach the handler to the logger
    if not logger.handlers:
        logger.addHandler(handler)

    return logger


# Initialize the logger
logger = setup_logging()
