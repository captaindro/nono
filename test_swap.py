import asyncio
import logging
from core.trading import try_buy_and_sell

# Configuration basique des logs pour console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("manual_test")

async def manual_test_token(token_address: str, creator_address: str = None):
    logger.info(f"🚀 Test manuel : lancement achat/revente pour token: {token_address} (creator: {creator_address})")
    await try_buy_and_sell(token_address, creator_address)

if __name__ == "__main__":
    # Remplace ici par une vraie adresse de token Pump.fun ou Dexscreener détectée
    token_frais = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
    creator_frais = "3m6V7F7XH39wG4EZ9LNd4Hzozj15SK17YaohbshTLWDp"

    logger.info("Début du test manuel avec token frais USDC")
    asyncio.run(manual_test_token(token_frais, creator_frais))
    logger.info("Fin du test manuel")
