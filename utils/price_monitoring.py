import asyncio
import logging
import httpx

logger = logging.getLogger(__name__)

async def get_price(input_mint: str, output_mint: str, amount: int) -> float:
    """
    Récupère le prix actuel d'un token via l'API Jupiter quote.
    """
    url = "https://quote-api.jup.ag/v6/quote"
    params = {
        "inputMint": input_mint,
        "outputMint": output_mint,
        "amount": amount,
        "slippageBps": 50,
        "onlyDirectRoutes": "true",
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        data = response.json()
        if "outAmount" in data and int(data["outAmount"]) > 0:
            price = int(data["outAmount"]) / amount
            return price
        else:
            logger.warning(f"[price_monitoring] Quote vide ou invalide pour {input_mint}")
            return 0.0

async def monitor_price_and_sell(token_info, buy_price: float, tp: float, sl: float):
    """
    Surveille le prix du token, et vend dès que take profit (tp) ou stop loss (sl) atteint.
    """
    mint = token_info.get("mint")
    logger.info(f"[monitor_price] Début monitoring prix pour {mint}, buy_price={buy_price}, TP={tp}, SL={sl}")

    output_mint = "So11111111111111111111111111111111111111112"  # SOL as output

    while True:
        current_price = await get_price(mint, output_mint, 10**9)
        logger.info(f"[monitor_price] Prix actuel de {mint}: {current_price}")

        if current_price >= tp * buy_price:
            logger.info(f"[monitor_price] TP atteint, vend token {mint} à {current_price}")
            # Ici lancer la vente (swap inverse) — simulé ici
            logger.info(f"[monitor_price] Vente simulée réussie pour {mint}")
            break
        elif current_price <= sl * buy_price:
            logger.info(f"[monitor_price] SL atteint, vend token {mint} à {current_price}")
            logger.info(f"[monitor_price] Vente simulée réussie pour {mint}")
            break

        await asyncio.sleep(5)  # Pause avant la prochaine vérification
