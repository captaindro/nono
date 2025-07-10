# utils/helpers.py

import asyncio
import logging
import time
from datetime import datetime
from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
from spl.token.instructions import get_associated_token_address

logger = logging.getLogger(__name__)

# ✅ Fonction ajoutée : mesure du temps écoulé
def seconds_since(start_time: float) -> float:
    """
    Retourne le nombre de secondes écoulées depuis `start_time` (issu de asyncio.get_event_loop().time())
    """
    return asyncio.get_event_loop().time() - start_time

# ✅ Timestamp formaté pour logs
def current_timestamp() -> str:
    """
    Retourne un timestamp formaté pour les logs ou fichiers (YYYY-MM-DD HH:MM:SS)
    """
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

# ✅ Conversion sécurisée float
def safe_float(value, default=0.0):
    """
    Tente de convertir une valeur en float, retourne `default` si erreur.
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

# ✅ Tronquage pour logs lisibles
def truncate_string(s: str, max_length: int = 12) -> str:
    """
    Tronque une chaîne de caractères trop longue avec '...' au milieu.
    """
    if len(s) <= max_length:
        return s
    return s[:max_length // 2] + "..." + s[-max_length // 2:]

# ✅ Déjà présent : métadonnées fictives de token
def get_token_metadata(token_address: str) -> dict:
    """
    Version synchrone — retourne des métadonnées fictives.
    À enrichir plus tard avec des appels à une vraie API (ex: Jupiter, Helius...).
    """
    return {
        "symbol": "???",
        "name": "Unknown Token",
        "decimals": 9,
        "address": token_address,
    }

# ✅ Déjà présent : solde réel du wallet pour un token SPL
async def get_token_balance(client: AsyncClient, owner_pubkey: str, token_mint: str) -> float:
    """
    Récupère le solde d'un token SPL pour un wallet donné.
    """
    try:
        owner = Pubkey.from_string(owner_pubkey)
        mint = Pubkey.from_string(token_mint)
        ata = get_associated_token_address(owner, mint)

        resp = await client.get_token_account_balance(ata)
        if resp.value:
            return float(resp.value.ui_amount_string)
    except Exception as e:
        logger.warning(f"[BALANCE] Erreur pour {token_mint} — {e}", exc_info=True)

    return 0.0
