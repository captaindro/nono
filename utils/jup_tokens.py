import httpx
import asyncio
import logging
from config.settings import settings
from rich import print

logger = logging.getLogger("jup_tokens")

JUPITER_API_URL = settings.jupiter_api_url
MAX_RETRIES = int(settings.max_retries)
RETRY_DELAY = int(settings.retry_delay_seconds)

async def is_token_tradable(token_address: str) -> bool:
    url = f"{JUPITER_API_URL}/token/{token_address}"
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(url)
                if resp.status_code == 200:
                    data = resp.json()
                    # On considère token tradable si on a un nom ou symbole
                    if data.get("name") and data.get("symbol"):
                        return True
                    return False
                elif resp.status_code == 429:
                    logger.warning(f"[JUP] 🚧 Rate limit atteinte pour {token_address} (tentative {attempt}/{MAX_RETRIES})")
                    await asyncio.sleep(RETRY_DELAY)
                else:
                    logger.warning(f"[JUP] HTTP {resp.status_code} pour {token_address}")
                    return False
        except Exception as e:
            logger.error(f"[JUP] Exception fetching token tradability {token_address}: {e}")
            await asyncio.sleep(RETRY_DELAY)
    return False
