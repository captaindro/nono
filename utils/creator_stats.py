import json
import os
from typing import Dict

CREATOR_STATS_FILE = "data/creator_stats.json"


def load_creator_stats() -> Dict[str, dict]:
    if not os.path.exists(CREATOR_STATS_FILE):
        return {}
    try:
        with open(CREATOR_STATS_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Erreur chargement {CREATOR_STATS_FILE} : {e}")
        return {}


def save_creator_stats(stats: Dict[str, dict]) -> None:
    os.makedirs(os.path.dirname(CREATOR_STATS_FILE), exist_ok=True)
    try:
        with open(CREATOR_STATS_FILE, "w") as f:
            json.dump(stats, f, indent=4)
    except Exception as e:
        print(f"[ERROR] Erreur écriture {CREATOR_STATS_FILE} : {e}")


def is_creator_blacklisted(creator_address: str) -> bool:
    stats = load_creator_stats()
    creator_info = stats.get(creator_address, {})
    return creator_info.get("blacklisted", False)


def is_known_rugger(creator_address: str) -> bool:
    stats = load_creator_stats()
    creator_info = stats.get(creator_address, {})
    return creator_info.get("rug", 0) > 0


def update_creator_stats(creator_address: str, success: bool) -> None:
    stats = load_creator_stats()
    entry = stats.get(creator_address, {"success": 0, "rug": 0})
    if success:
        entry["success"] += 1
    else:
        entry["rug"] += 1

    if entry["rug"] >= 2 and entry["success"] == 0:
        entry["blacklisted"] = True

    stats[creator_address] = entry
    save_creator_stats(stats)


def add_new_creator_if_missing(creator_address: str) -> None:
    stats = load_creator_stats()
    if creator_address not in stats:
        stats[creator_address] = {"success": 0, "rug": 0}
        save_creator_stats(stats)


def add_suspect_creator(creator_address: str) -> None:
    """
    Marque un créateur comme 'suspect', utile quand le score est mauvais mais qu’on veut le suivre.
    """
    stats = load_creator_stats()
    entry = stats.get(creator_address, {"success": 0, "rug": 0})
    entry["suspect"] = True
    stats[creator_address] = entry
    save_creator_stats(stats)
