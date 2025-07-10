# utils/filters.py

import logging
from config.settings import settings
from core.creator_db import compute_creator_score

log = logging.getLogger(__name__)

def token_passes_filters(creator_address: str, liquidity: float, token_score: float) -> bool:
    """
    Applique les filtres de base sur un token avant sniping :
    - Score du créateur
    - Liquidité minimale
    - Score token (ex: honeypot / scam)
    """
    if liquidity < settings.liquidity_threshold_sol:
        log.warning(f"❌ Token ignoré : liquidité trop faible ({liquidity:.3f} SOL)")
        return False

    if token_score < settings.token_score_threshold:
        log.warning(f"❌ Token ignoré : score trop bas ({token_score:.2f})")
        return False

    score = compute_creator_score(creator_address)
    if score < 0.3:  # seuil personnalisable
        log.warning(f"❌ Token ignoré : créateur à score suspect ({score:.2f})")
        return False

    log.info(f"✅ Token validé : score créateur={score:.2f} | score token={token_score:.2f} | liquidité={liquidity:.3f} SOL")
    return True
