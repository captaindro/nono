<<<<<<< HEAD
import json
from collections import defaultdict
from pathlib import Path

TRACKER_FILE = Path("creator_stats.json")

if not TRACKER_FILE.exists():
    TRACKER_FILE.write_text(json.dumps({}))
def mark_token_as_rug(creator: str):
    """
    Marque un wallet comme rugger confirmé (score élevé forcé).
    """
    stats = load_stats()
    creator_data = stats.get(creator, {"count": 0, "last": time.time(), "score": 0})
    creator_data["score"] = 100  # Score très élevé
    stats[creator] = creator_data
    save_stats(stats)
    log.info(f"💀 Rug confirmé : {creator} → score mis à 100")

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
=======
import logging

logger = logging.getLogger("creator_tracker")

# Exemple simplifié d'un tracker des créateurs suspects
class CreatorTracker:
    def __init__(self):
        # Cette liste devrait être chargée depuis un fichier ou base persistante
        self.suspicious_creators = set([
            "SomeSuspiciousWalletAddress1",
            "SomeSuspiciousWalletAddress2",
            # ... ajouter les autres créateurs suspects
        ])

    def is_suspicious(self, creator_address: str) -> bool:
        return creator_address in self.suspicious_creators

creator_tracker = CreatorTracker()

def get_creator_info(creator_address: str):
    # Exemple : retourne un dict avec infos sur le créateur
    # Ici simplifié, tu peux étendre avec plus de données
    is_rugger = creator_tracker.is_suspicious(creator_address)
    info = {
        "address": creator_address,
        "is_rugger": is_rugger,
    }
    logger.debug(f"Créateur info pour {creator_address}: {info}")
    return info

def is_rugger(creator_address: str) -> bool:
    return creator_tracker.is_suspicious(creator_address)
>>>>>>> 2553739 (Ajout de la config Railway et du workflow CI/CD)
