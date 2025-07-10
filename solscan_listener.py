import asyncio
import httpx
import logging
from datetime import datetime

logger = logging.getLogger("solscan_listener")

SOLSCAN_API_URL = "https://public-api.solscan.io/token/creation"
POLL_INTERVAL_SECONDS = 5  # fréquence d'interrogation de l'API

_seen_tokens = set()

async def fetch_new_tokens():
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            resp = await client.get(SOLSCAN_API_URL)
            resp.raise_for_status()
            data = resp.json()
            # data attendu sous forme liste de dicts [{tokenAddress, creatorAddress, timestamp}, ...]
            return data
        except Exception as e:
            logger.error(f"[Solscan] Erreur fetching tokens: {e}")
            return []

async def start_solscan_listener(callback):
    logger.info("Listener Solscan démarré, récupération des tokens récents...")

    while True:
        tokens = await fetch_new_tokens()

        new_tokens = []
        for token_info in tokens:
            token_address = token_info.get("tokenAddress")
            creator_address = token_info.get("creatorAddress")

            if token_address is None or creator_address is None:
                continue
            if token_address in _seen_tokens:
                continue
            _seen_tokens.add(token_address)
            new_tokens.append((token_address, creator_address))

        if new_tokens:
            logger.info(f"[Solscan] {len(new_tokens)} nouveau(x) token(s) détecté(s)")

            for token_address, creator_address in new_tokens:
                try:
                    await callback(token_address, creator_address)
                except Exception as e:
                    logger.error(f"[Solscan] Erreur dans callback pour {token_address}: {e}")

        else:
            logger.info(f"[Solscan] Aucun nouveau token détecté à {datetime.utcnow().isoformat()}")

        await asyncio.sleep(POLL_INTERVAL_SECONDS)
