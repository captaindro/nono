import json
from config.settings import settings
from utils.jup_swap import execute_swap
from utils.csv_logger import log_transaction_csv
from wallets.wallet_manager import get_wallet_pubkey_from_path
from loguru import logger as log


async def sell_token(token_address: str, amount: str, wallet_path: str, simulate_only: bool = False, origin_tx: str = None):
    """
    Vend un token donné pour 100% (par défaut), en utilisant Jupiter swap.
    """
    log.info(f"[SELL] Tentative de revente de {amount} du token {token_address}")

    # Toujours depuis token vers SOL
    input_mint = token_address
    output_mint = "So11111111111111111111111111111111111111112"  # SOL

    result = await execute_swap(
        input_mint=input_mint,
        output_mint=output_mint,
        amount=amount,
        slippage=settings.SLIPPAGE_BPS,
        wallet_path=wallet_path,
        simulate_only=simulate_only,
    )

    if not result:
        log.warning(f"[SELL] ❌ Revente échouée pour {token_address}")
        return

    log.success(f"[SELL] ✅ Revente réussie pour {token_address}")

    if settings.CSV_OUTPUT_ENABLED:
        try:
            wallet_pubkey = get_wallet_pubkey_from_path(wallet_path)
            log_transaction_csv(
                token_address=token_address,
                profit_amount=None,  # À calculer plus tard
                wallet_used=wallet_pubkey,
                origin_tx=origin_tx,
                swap_tx=result,
                sell=True
            )
        except Exception as e:
            log.exception(f"[SELL] ⚠️ Erreur lors du log CSV : {e}")
