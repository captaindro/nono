# utils/rugwatch.py

import json
from pathlib import Path

STATS_PATH = Path("creator_stats.json")

def load_stats():
    if STATS_PATH.exists():
        return json.loads(STATS_PATH.read_text())
    return {}

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
