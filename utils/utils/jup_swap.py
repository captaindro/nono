import logging
import asyncio

log = logging.getLogger(__name__)

async def buy_token(mint_address: str, amount_sol: float) -> str:
    log.info(f"🛒 Achat simulé de {amount_sol} SOL sur le token {mint_address}")
    await asyncio.sleep(1)
    return f"fake-buy-txid-{mint_address}"

async def sell_token(mint: str, amount: float):
    log.info(f"💰 Vente simulée de {amount} {mint}")
    await asyncio.sleep(1)
    return True