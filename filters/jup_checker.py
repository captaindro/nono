import os
import json
import time
import httpx
import logging
from config.settings import settings

logger = logging.getLogger("jup_checker")

# Fichier pour éviter de retester les tokens non tradables
UNTRADABLE_PATH = os.path.join(os.path.dirname(__file__), "../cache/untradable_tokens.json")
CREATOR_STATS_PATH = os.path.join(os.path.dirname(__file__), "../creator_stats.json")

# Quote WSOL (Solana wrapped native token)
WSOL_MINT = "So11111111111111111111111111111111111111112"


def load_json(path: str) -> dict:
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def save_json(path: str, data: dict):
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        logger.error(f"[jup_checker] ❌ Erreur d'écriture dans {path} : {e}")


def is_recently_marked_untradable(token_address: str) -> bool:
    data = load_json(UNTRADABLE_PATH)
    entry = data.get(token_address)
    if not entry:
        return False
    timestamp = entry.get("timestamp", 0)
    return time.time() - timestamp < settings.retry_delay_seconds


def mark_token_untradable(token_address: str):
    data = load_json(UNTRADABLE_PATH)
    data[token_address] = {"timestamp": int(time.time())}
    save_json(UNTRADABLE_PATH, data)


def update_creator_stats(creator_address: str):
    data = load_json(CREATOR_STATS_PATH)
    if creator_address not in data:
        data[creator_address] = {
            "count": 1,
            "score": 30,
            "label": "AUTO_FLAGGED"
        }
    else:
        data[creator_address]["count"] += 1
    save_json(CREATOR_STATS_PATH, data)


async def is_token_tradable(token_address: str, creator_address: str) -> bool:
    if is_recently_marked_untradable(token_address):
        logger.warning(f"[jup_checker] ⏩ Token {token_address} récemment marqué comme non tradable. Skipping.")
        return False

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            url = f"https://quote-api.jup.ag/v6/quote"
            params = {
                "inputMint": WSOL_MINT,
                "outputMint": token_address,
                "amount": int(float(settings.quote_amount) * 1e9),
                "slippageBps": settings.slippage_bps,
                "swapMode": "ExactIn"
            }
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if not data.get("routePlan"):
                raise ValueError("RoutePlan vide")

            return True

    except Exception as e:
        logger.warning(f"[jup_checker] 🚫 Token {token_address} non tradable via Jupiter : {e}")
        mark_token_untradable(token_address)
        update_creator_stats(creator_address)
        return False
