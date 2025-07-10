import json
import os
from typing import Dict, Optional
from config.settings import settings
from loguru import logger as log

# ✅ Chemin vers le fichier JSON
CREATOR_STATS_PATH = os.path.join(settings.base_path, "creator_stats.json")

# Structure type du fichier JSON :
# {
#   "CREATOR_ADDRESS": {
#       "total_tokens": 3,
#       "rugged_tokens": 2,
#       "safe_tokens": 1,
#       ...
#   },
#   ...
# }

def load_creator_stats() -> Dict[str, Dict]:
    if not os.path.exists(CREATOR_STATS_PATH):
        return {}
    with open(CREATOR_STATS_PATH, "r") as f:
        return json.load(f)

def save_creator_stats(stats: Dict[str, Dict]) -> None:
    with open(CREATOR_STATS_PATH, "w") as f:
        json.dump(stats, f, indent=2)

def update_creator_stats(creator: str, rugged: bool) -> None:
    stats = load_creator_stats()
    if creator not in stats:
        stats[creator] = {
            "total_tokens": 0,
            "rugged_tokens": 0,
            "safe_tokens": 0,
        }

    stats[creator]["total_tokens"] += 1
    if rugged:
        stats[creator]["rugged_tokens"] += 1
    else:
        stats[creator]["safe_tokens"] += 1

    save_creator_stats(stats)

def get_creator_stats(creator: str) -> Optional[Dict]:
    stats = load_creator_stats()
    return stats.get(creator)

def compute_creator_score(creator: str) -> float:
    stats = get_creator_stats(creator)
    if not stats:
        return 0.0

    total = stats.get("total_tokens", 0)
    rugged = stats.get("rugged_tokens", 0)

    if total == 0:
        return 0.0

    ratio = rugged / total
    score = round(ratio * 100, 2)  # Ex: 66.67
    return score

def is_creator_suspicious(creator: str) -> bool:
    score = compute_creator_score(creator)
    return score >= settings.token_score_threshold

def is_suspect_creator(creator: str) -> bool:
    try:
        if not creator or creator.upper() in ["CREATOR", "UNKNOWN"]:
            return False
        return is_creator_suspicious(creator)
    except Exception as e:
        log.exception(f"[CREATOR] Erreur dans is_suspect_creator : {e}")
        return False

# ✅ Récupération du créateur d’un token via RPC Helius
from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey


async def get_token_creator(token_address: str) -> str:
    """
    Récupère le créateur d’un token en lisant son compte via RPC Helius.
    """
    try:
        async with AsyncClient(settings.rpc_helius) as client:
            resp = await client.get_account_info(PublicKey(token_address))
            info = resp.value
            if not info or "owner" not in info:
                raise ValueError("Aucune donnée pour ce token")
            return str(info["owner"])
    except Exception as e:
        log.exception(f"[CREATOR] Erreur lors de la récupération du créateur du token {token_address}")
        return "UNKNOWN"
