<<<<<<< HEAD
# utils/reinvest.py

import os
import json
from pathlib import Path

STATE_FILE = Path('state.json')

def load_state() -> dict:
    """
    Charge l’état courant (balance réinvestissable) depuis state.json.
    """
    if STATE_FILE.exists():
        with STATE_FILE.open() as f:
            return json.load(f)
    return {"balance": 0}

def save_state(state: dict):
    """
    Sauvegarde l’état mis à jour (balance) dans state.json.
    """
    with STATE_FILE.open('w') as f:
        json.dump(state, f)

def get_reinvest_amount(base_amount: int, settings: dict) -> int:
    """
    Si reinvest activé, ajoute la balance stockée au montant de base.
    Sinon renvoie base_amount.
    """
    state = load_state()
    if not settings['jupiter'].get('reinvest', False):
        return base_amount
    return base_amount + int(state.get('balance', 0))

def record_gain(gain: float):
    """
    Ajoute le gain (en lamports de SOL) à la balance et sauve l’état.
    """
    state = load_state()
    state['balance'] = state.get('balance', 0) + gain
    save_state(state)
=======
import logging

logger = logging.getLogger(__name__)

def reinvest_profits(profits_amount: float, reinvest_percentage: float) -> float:
    """
    Calcule la somme à réinvestir en fonction des profits et du pourcentage de réinvestissement.
    """
    reinvest_amount = profits_amount * (reinvest_percentage / 100)
    logger.info(f"[reinvest] Montant réinvesti: {reinvest_amount} sur profits de {profits_amount}")
    return reinvest_amount
>>>>>>> 2553739 (Ajout de la config Railway et du workflow CI/CD)
