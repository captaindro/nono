import json
import os

def is_rugger(wallet_address: str) -> bool:
    """
    Retourne True si le wallet est identifié comme rugger dans creator_stats.json
    """
    try:
        with open("data/creator_stats.json", "r") as f:
            stats = json.load(f)
        creator_info = stats.get(wallet_address, {})
        return creator_info.get("is_rugger", False)
    except Exception:
        return False
