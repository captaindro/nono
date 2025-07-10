# debug_quote.py

import os, json, httpx, asyncio
from dotenv import load_dotenv
from loguru import logger
from solders.keypair import Keypair

load_dotenv()

async def main():
    # Charger settings
    JUP_URL = os.getenv("JUPITER_API_URL")
    SLIPPAGE = int(os.getenv("SLIPPAGE_BPS", "50"))
    ONLY_DIRECT = os.getenv("JUPITER_ONLY_DIRECT_ROUTES", "false").lower() == "true"

    # Charger wallet pour userPublicKey
    with open("wallets/walletpapy.json", "r") as f:
        secret = json.load(f)
    kp = Keypair.from_bytes(bytes(secret))
    USER_PUB = str(kp.pubkey())

    params = {
        "amount": str(100_000_000),  # 0.1 SOL
        "inputMint": "So11111111111111111111111111111111111111112",
        "outputMint": "EPjFWdd5AufqSSqeM2qiwpKjfHb2ThYSuYeZ3JC9Sm31",
        "slippageBps": SLIPPAGE,
        "onlyDirectRoutes": ONLY_DIRECT,
        "userPublicKey": USER_PUB,
    }

    logger.info(f"🔎 GET {JUP_URL}/v6/quote")
    logger.info(json.dumps(params, indent=2))

    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(f"{JUP_URL}/v6/quote", params=params)
        logger.info(f"📥 Status: {resp.status_code}")
        logger.info(f"Body: {resp.text}")

if __name__ == "__main__":
    asyncio.run(main())
