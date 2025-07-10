<<<<<<< HEAD
# utils/scoring.py

import numpy as np

def score_token(liquidity: float, volatility: float, age_seconds: float) -> float:
    """
    Calcule un score de potentiel pour un token basé sur :
      - liquidity (SOL)
      - volatility (écart-type du prix)
      - age_seconds (temps écoulé depuis création)

    Les poids et la formule sont à affiner avec votre modèle IA.
    Retourne un float entre 0.0 (pas intéressant) et 1.0 (très prometteur).
    """
    # Normalisation simple
    liq_norm = min(liquidity / 10.0, 1.0)
    vol_norm = min(volatility / 0.05, 1.0)  # 5 % std dev
    age_norm = 1.0 - np.tanh(age_seconds / 3600.0)  # on privilégie les tokens jeunes

    # Poids initiaux
    w_liq, w_vol, w_age = 0.5, 0.3, 0.2

    score = w_liq * liq_norm + w_vol * vol_norm + w_age * age_norm
    # On clamp entre 0 et 1
    return float(max(0.0, min(1.0, score)))
=======
import logging
from utils.token_metadata import get_token_metadata

logger = logging.getLogger("scoring")

async def score_token(token_address: str) -> float:
    """
    Calcule un score simple basé sur les métadonnées.
    Peut être amélioré plus tard avec un vrai modèle.
    """
    try:
        metadata = await get_token_metadata(token_address)
        score = 0

        if metadata.get("symbol"):
            score += 20
        if metadata.get("name"):
            score += 20
        if metadata.get("description"):
            score += 10
        if metadata.get("socials"):
            score += 50  # Présence de réseaux sociaux = bon signal

        logger.debug(f"[SCORING] Score du token {token_address} : {score}")
        return score
    except Exception as e:
        logger.error(f"[SCORING] Erreur lors du scoring de {token_address} : {e}", exc_info=True)
        return 0
>>>>>>> 2553739 (Ajout de la config Railway et du workflow CI/CD)
