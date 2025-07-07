# utils/rugwatch.py

import json
from pathlib import Path

STATS_PATH = Path("creator_stats.json")

def load_stats() -> dict:
    if not os.path.exists(CREATOR_STATS_PATH):
        return {}
    with open(CREATOR_STATS_PATH, "r") as f:
        return json.load(f)

def save_stats(stats):
    STATS_PATH.write_text(json.dumps(stats, indent=2))

def record_token_creation(wallet: str, token: str):
    stats = load_stats()
    wallet_stats = stats.get(wallet, {"tokens": [], "count": 0})

    wallet_stats["tokens"].append(token)
    wallet_stats["count"] += 1

    stats[wallet] = wallet_stats
    save_stats(stats)

def is_suspicious(wallet: str, threshold: int = 5) -> bool:
    stats = load_stats()
    wallet_stats = stats.get(wallet)
    if not wallet_stats:
        return False
    return wallet_stats["count"] >= threshold

def mark_token_as_rug(creator_wallet: str):
    from utils.creator_tracker import record_token_creation
    record_token_creation(creator_wallet, is_rug=True)
