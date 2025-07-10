import asyncio
import logging

logger = logging.getLogger("token_liquidity")

async def has_sufficient_liquidity(token_address: str, threshold_sol: float = 0.3) -> bool:
    # Simplifié : toujours True pour test, à remplacer par vraie vérif liquidité
    logger.info(f"[LIQ] Vérification liquidité pour {token_address} avec seuil {threshold_sol} SOL")
    await asyncio.sleep(0.1)
    return True
