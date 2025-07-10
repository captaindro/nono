import asyncio
import logging
from utils.trade import handle_token

# Configuration du logging
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Token connu : USDC
USDC_TOKEN = {
    "mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
    "symbol": "USDC",
    "name": "USD Coin",
    "score": 1.0,
    "liquidity": 10000.0,
}

async def main():
    logger.info("🔬 Lancement du test avec token liquide : USDC")
    await handle_token(USDC_TOKEN, force_buy=True)
    logger.info("✅ Test terminé")

if __name__ == "__main__":
    asyncio.run(main())
