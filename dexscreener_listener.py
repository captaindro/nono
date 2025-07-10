import asyncio
import httpx
import logging
from rich.logging import RichHandler

logger = logging.getLogger("dexscreener")
logger.setLevel(logging.INFO)
logger.addHandler(RichHandler(rich_tracebacks=True, markup=True))

DEXSCREENER_URL = "https://api.dexscreener.com/latest/dex/tokens/solana"
FETCH_INTERVAL = 5  # secondes entre chaque fetch


async def start_dexscreener_listener(callback):
    async with httpx.AsyncClient(timeout=10.0) as client:
        while True:
            try:
                response = await client.get(DEXSCREENER_URL, follow_redirects=True)
                response.raise_for_status()
                data = response.json()
                tokens = data.get("tokens", [])

                if not tokens:
                    logger.info("[dexscreener] Aucun nouveau token détecté")
                else:
                    logger.info(f"[dexscreener] {len(tokens)} tokens détectés")

                # Parcours et callback sur chaque token detecté
                for token in tokens:
                    address = token.get("address")
                    creator = token.get("creator") or "Unknown"
                    if address:
                        await callback(address, creator)

            except httpx.HTTPStatusError as e:
                logger.error(f"[dexscreener] Erreur HTTP : {e.response.status_code} - {e.response.text}")
            except Exception as e:
                logger.error(f"[dexscreener] Erreur fetching tokens: [red]{e}[/red]", exc_info=True)

            await asyncio.sleep(FETCH_INTERVAL)
