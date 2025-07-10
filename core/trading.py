import asyncio
import random
from loguru import logger

from config.settings import settings
from utils.token_utils import get_token_liquidity
from utils.jup_swap import execute_swap
from utils.sell_token import sell_token
from core.creator_db import is_suspect_creator
from wallets.wallet_manager import get_random_wallet

MAX_RETRIES = settings.max_retries
RETRY_DELAY = settings.retry_delay_seconds


async def try_buy_and_sell(token_address: str, creator_address: str):
    logger.info(f"[TEST] Tentative d'achat/revente du token {token_address}")

    # Vérification du créateur
    if is_suspect_creator(creator_address):
        logger.warning(f"[TEST] Créateur {creator_address} reconnu comme rugger ✅")
    else:
        if not settings.force_buy_mode:
            logger.warning(f"[TEST] Créateur {creator_address} non reconnu comme rugger.")
            return
        logger.warning(f"[TEST] [FORCE] Achat autorisé pour {creator_address} même s'il n'est pas marqué rugger.")

    # Vérification de la liquidité avec retry si 400 Jupiter
    for attempt in range(1, MAX_RETRIES + 1):
        result = await get_token_liquidity(token_address)
        if result and result.get("can_buy"):
            logger.info(f"[JUPITER] ✅ Token tradable trouvé à la tentative {attempt}")
            break
        else:
            logger.warning(f"[RETRY] Token non tradable (tentative {attempt}/{MAX_RETRIES})")
            await asyncio.sleep(RETRY_DELAY)
    else:
        logger.warning(f"[TEST] Liquidité insuffisante pour {token_address} après {MAX_RETRIES} tentatives")
        return

    # Achat via Jupiter
    wallet = get_random_wallet()
    buy_result = await execute_swap(token_address, wallet, simulate_only=settings.simulate_only)

    if not buy_result or not buy_result.get("txid"):
        logger.error(f"[SWAP] ❌ Achat échoué pour {token_address}")
        return

    logger.success(f"[SWAP] ✅ Achat réussi pour {token_address}, tx: {buy_result['txid']}")

    # Revente immédiate (100%)
    await asyncio.sleep(3)
    await sell_token(token_address, amount=1.0, wallet=wallet)
