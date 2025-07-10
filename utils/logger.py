# utils/logger.py

import logging
from rich.logging import RichHandler

def get_logger(name: str) -> logging.Logger:
    """
    Crée ou récupère un logger enrichi avec RichHandler pour un affichage propre.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        handler = RichHandler(rich_tracebacks=True)
        formatter = logging.Formatter(
            "%(message)s",
            datefmt="[%X]"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False

    return logger
