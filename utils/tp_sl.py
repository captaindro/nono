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
def should_sell(buy_price, current_price, tp_multiplier=1.5, sl_multiplier=0.8):
    """
    Détermine s'il faut vendre en fonction des take profit (TP) et stop loss (SL).
    """
    if current_price >= buy_price * tp_multiplier:
        return True, "TP atteint"
    elif current_price <= buy_price * sl_multiplier:
        return True, "SL atteint"
    else:
        return False, "Condition non atteinte"
