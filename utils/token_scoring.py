import asyncio
import logging

logger = logging.getLogger("token_scoring")

async def calculate_token_score(token_address: str, creator_address: str = None) -> float:
    # Simplifié : score fixe à 1.0 pour test, à remplacer par algo réel
    logger.info(f"[SCORE] Calcul du score pour token {token_address} (creator: {creator_address})")
    await asyncio.sleep(0.1)
    return 1.0
