import time
import logging
import asyncio

from main import handle_new_token

# Configure le logging si ce n’est pas fait
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")

# Mint du token à tester (remplace par un mint réel de Pump.fun)
token_mint = "EPCtgmcgkvhhn63iyqbfrpjkyesvkooxf8zi9vdoac4j"

async def test_manual_mint():
    print(f"🚀 Test achat/revente forcé sur {token_mint}")
    await handle_new_token(token_mint, time.time())

if __name__ == "__main__":
    asyncio.run(test_manual_mint())
