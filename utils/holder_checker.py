# utils/holder_checker.py
import asyncio
import httpx
from utils.config import RPC_URL
from utils.logger import get_logger

logger = get_logger("holder_checker")


async def check_holders(token_mint: str, max_holders: int = 100) -> bool:
    """
    Vérifie si le nombre de holders dépasse un seuil.
    Cette version retourne True (safe) par défaut pour test.
    """
    try:
        # Stub : simulateur de récupération des holders
        holders_count = 10  # valeur fictive
        logger.debug(f"[holders] {token_mint} a {holders_count} holders.")

        if holders_count > max_holders:
            logger.warning(f"[holders] Trop de holders pour {token_mint} : {holders_count}")
            return False

        return True

    except Exception as e:
        logger.error(f"[holders] Erreur lors du check holders : {e}")
        return False
