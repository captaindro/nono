import asyncio
from loguru import logger
from utils.filters import is_honeypot, has_sufficient_liquidity
from utils.metadata import fetch_token_metadata
from utils.jup_swap import execute_swap
from utils.token_utils import get_token_creator
from utils.csv_logger import save_trade_to_csv
from utils.creator_stats import is_known_rugger
from utils.scoring import score_token
from wallets.wallet_manager import get_random_wallet
from config.settings import (
    TAKE_PROFIT_MULTIPLIER,
    STOP_LOSS_MULTIPLIER,
    SLIPPAGE_BPS,
    TOKEN_SCORE_THRESHOLD,
    LIQUIDITY_THRESHOLD_SOL,
    QUOTE_AMOUNT,
)


async def sniping_pipeline(token_data: dict):
    logger.info(f"🚀 Nouveau token détecté : {token_data}")

    try:
        result = token_data.get("result")
        if not isinstance(result, dict) or "data" not in result or "mint" not in result["data"]:
            logger.warning(f"⚠️ Données de token invalides ou incomplètes : {result}")
            return

        mint_address = result["data"]["mint"]

        # 1. Check honeypot
        if await is_honeypot(mint_address):
            logger.warning(f"🚫 Token honeypot détecté : {mint_address}")
            return

        # 2. Check liquidité
        if not await has_sufficient_liquidity(mint_address, LIQUIDITY_THRESHOLD_SOL):
            logger.warning(f"💧 Liquidité insuffisante pour {mint_address}")
            return

        # 3. Vérifie si rugger connu
        creator = await get_token_creator(mint_address)
        if creator and await is_known_rugger(creator):
            logger.warning(f"⚠️ Créateur {creator} identifié comme rugger. Skip.")
            return

        # 4. Récupère les métadonnées
        metadata = await fetch_token_metadata(mint_address)
        if not metadata:
            logger.warning(f"❌ Impossible de récupérer les métadonnées pour {mint_address}")
            return

        symbol = metadata.get("symbol", "???")
        name = metadata.get("name", "???")

        # 5. Scoring
        score = score_token({"liquidity": metadata.get("liquidity", 0), "symbol": symbol})
        logger.info(f"📊 Score du token {mint_address} : {score}")
        if score < TOKEN_SCORE_THRESHOLD:
            logger.warning(f"⛔ Score trop bas pour {mint_address} ({score})")
            return

        # 6. Swap achat
        wallet = get_random_wallet()
        amount_in = QUOTE_AMOUNT

        tx_buy = await execute_swap(
            input_mint="So11111111111111111111111111111111111111112",  # WSOL
            output_mint=mint_address,
            amount=amount_in,
            wallet=wallet,
            slippage_bps=SLIPPAGE_BPS,
        )

        if not tx_buy or tx_buy.get("error"):
            logger.error(f"❌ Swap d'achat échoué pour {mint_address}")
            return

        logger.success(f"✅ Achat réussi du token {mint_address} via Jupiter")

        # 7. Swap vente immédiate (take profit ou SL peuvent s'ajouter ici)
        tx_sell = await execute_swap(
            input_mint=mint_address,
            output_mint="So11111111111111111111111111111111111111112",  # WSOL
            amount="ALL",  # Revente complète
            wallet=wallet,
            slippage_bps=SLIPPAGE_BPS,
        )

        if not tx_sell or tx_sell.get("error"):
            logger.error(f"❌ Swap de vente échoué pour {mint_address}")
            return

        logger.success(f"💰 Token {mint_address} revendu avec succès !")
        amount_out = tx_sell.get("amount_out", 0)

        # 8. Log CSV
        save_trade_to_csv(token_address=mint_address, token_name=name, symbol=symbol, amount_out=amount_out)

    except Exception as e:
        logger.error(f"Erreur dans le pipeline pour {token_data} : {e}", exc_info=True)
