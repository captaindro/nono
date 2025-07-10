import logging
from rich.logging import RichHandler

def get_logger():
    FORMAT = "%(message)s"
    logging.basicConfig(
        level=logging.DEBUG,
        format=FORMAT,
        datefmt="[%X]",
        handlers=[RichHandler()]
    )
