import asyncio
import logging
from utils.swap import execute_sell

log = logging.getLogger(__name__)

async def monitor_token(token_address: str, buy_amount_lamports: int, buy_price: float):
    """
    Revente automatique après 3 secondes, utilisée pour tests ou stratégie rapide.
    """
    log.info(f"⏱️ Attente 3s avant revente du token {token_address}")
    await asyncio.sleep(3)
    
    try:
        tx = await execute_sell(token_address)
        log.info(f"✅ Token {token_address} revendu avec succès : {tx}")
    except Exception as e:
        log.error(f"❌ Erreur lors de la revente de {token_address} : {e}")
