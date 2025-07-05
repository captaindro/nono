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
