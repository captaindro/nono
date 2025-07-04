# utils/monitor.py

import asyncio
import logging
from utils.jupiter import execute_swap
from utils.reinvest import record_gain

async def monitor_position(sig_in: str,
                           tp: float,
                           sl: float,
                           timeout_seconds: int,
                           token_mint: str,
                           amount: int,
                           settings: dict):
    """
    Surveille la position jusqu'à TP, SL ou timeout, puis swap token->SOL
    et enregistre le gain si reinvest activé.
    """
    start = asyncio.get_event_loop().time()
    logging.info(f"▶️ Surveillance position: TP={tp:.6f}, SL={sl:.6f}, timeout={timeout_seconds}s")

    async def get_current_price() -> float:
        # TODO : récupérer via on-chain ou oracle
        return tp  # stub : simule TP atteint

    while True:
        elapsed = asyncio.get_event_loop().time() - start
        if elapsed >= timeout_seconds:
            logging.info("⏱️ Timeout atteint, clôture position")
            break

        price = await get_current_price()
        if price >= tp:
            logging.info("🔼 TP atteint, clôture position")
            break
        if price <= sl:
            logging.info("🔽 SL atteint, clôture position")
            break

        await asyncio.sleep(1)

    # Exécuter le swap inverse : token -> SOL
    sig_out, sell_expected = execute_swap(
        input_mint=token_mint,
        output_mint="So11111111111111111111111111111111111111112",
        amount=amount,
        slippage_bps=settings['jupiter']['slippage_bps']
    )
    logging.info(f"✅ Position clôturée, signature sell: {sig_out}")

    # Calcul et enregistrement du gain (lamports)
    gain = sell_expected - amount
    if settings['jupiter'].get('reinvest', False):
        record_gain(gain)
        logging.info(f"💰 Gain de {gain} lamports enregistré pour réinvestissement")
