import sys
from utils.logger import get_logger

logger = get_logger("guard")

def stop_bot(reason: str):
    logger.critical(f"[CRITICAL] Arrêt immédiat du bot : {reason}")
    sys.exit(1)
