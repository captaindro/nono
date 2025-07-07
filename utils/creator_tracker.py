import json
from collections import defaultdict
from pathlib import Path

TRACKER_FILE = Path("creator_stats.json")

if not TRACKER_FILE.exists():
    TRACKER_FILE.write_text(json.dumps({}))


def load_data():
    return json.loads(TRACKER_FILE.read_text())


def save_data(data):
    TRACKER_FILE.write_text(json.dumps(data, indent=2))


def record_token_creation(wallet: str, is_rug: bool):
    data = load_data()
    wallet_data = data.get(wallet, {"created": 0, "rugged": 0})
    wallet_data["created"] += 1
    if is_rug:
        wallet_data["rugged"] += 1
    data[wallet] = wallet_data
    save_data(data)


def get_creator_score(wallet: str) -> float:
    data = load_data()
    wallet_data = data.get(wallet)
    if not wallet_data:
        return 1.0  # unknown creator, neutral
    created = wallet_data["created"]
    rugged = wallet_data["rugged"]
    if created == 0:
        return 1.0
    return max(0.0, 1.0 - (rugged / created))


def is_suspicious(wallet: str, threshold: float = 0.4) -> bool:
    return get_creator_score(wallet) < threshold
