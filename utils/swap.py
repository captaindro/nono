# utils/swap.py

import logging
import asyncio

log = logging.getLogger(__name__)

async def execute_sell(token_address: str) -> str:
    """
    Simulation d'une vente de token. À remplacer par la vraie intégration Jupiter.
    """
    log.info(f"💰 Simulation de la revente du token {token_address}")
    await asyncio.sleep(1)  # Simule un délai réseau
    return f"fake-txid-for-{token_address}"
