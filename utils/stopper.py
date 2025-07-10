import sys
import logging
from utils.logger import get_logger


logger = get_logger("stopper")

def stop_bot(reason: str = "Arrêt demandé"):
    """
    Stoppe proprement l’exécution du bot avec un message de log.
    """
    logger.critical(f"🛑 BOT ARRÊTÉ : {reason}")
    sys.exit(1)
