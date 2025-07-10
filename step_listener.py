import asyncio
import httpx
import logging
from datetime import datetime

logger = logging.getLogger("step_listener")

STEP_API_URL = "https://api.step.finance/api/tokens/recent"  # Hypothétique, à vérifier ou adapter
POLL_INTERVAL_SECONDS = 6  # Intervalle de polling

_seen_tokens = set()

async def fetch_step_tokens():
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            resp = await client.get(STEP_API_URL)
            resp.raise_for_status()
            data = resp.json()
            # Hypothèse : data = {"tokens": [{"address": ..., "creator": ...}, ...]}
            return data.get("tokens", [])
        except Exception as e:
            logger.error(f"[StepFinance] Erreur fetching tokens: {e}")
            return []

async def start_step_listener(callback):
    logger.info("Listener Step Finance démarré, récupération des tokens récents...")

    while True:
        tokens = await fetch_step_tokens()

        new_tokens = []
        for token_info in tokens:
            token_address = token_info.get("address")
            creator_address = token_info.get("creator")

            if not token_address or not creator_address:
                continue
            if token_address in _seen_tokens:
                continue
            _seen_tokens.add(token_address)
            new_tokens.append((token_address, creator_address))

        if new_tokens:
            logger.info(f"[StepFinance] {len(new_tokens)} nouveau(x) token(s) détecté(s)")

            for token_address, creator_address in new_tokens:
                try:
                    await callback(token_address, creator_address)
                except Exception as e:
                    logger.error(f"[StepFinance] Erreur dans callback pour {token_address}: {e}")

        else:
            logger.info(f"[StepFinance] Aucun nouveau token détecté à {datetime.utcnow().isoformat()}")

        await asyncio.sleep(POLL_INTERVAL_SECONDS)
