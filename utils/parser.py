# utils/parser.py

import json
import time
import logging
from typing import Any, Optional, Tuple

log = logging.getLogger("nono.parser")

def _find_pubkey(obj: Any) -> Optional[str]:
    """
    Parcourt récursivement un dict ou list pour trouver la première valeur associée à la clé 'pubkey'.
    """
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "pubkey" and isinstance(v, str):
                return v
            found = _find_pubkey(v)
            if found:
                return found
    elif isinstance(obj, list):
        for item in obj:
            found = _find_pubkey(item)
            if found:
                return found
    return None

def parse_msg(raw: str) -> Tuple[str, float]:
    """
    Parse un message JSON brut provenant du WebSocket Helius Pump.fun.
    Renvoie toujours (token_address, timestamp).

    Cherche simplement la première occurence de 'pubkey' dans le message.
    """
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON invalide: {e}")

    token_address = _find_pubkey(data)
    if not token_address:
        log.debug(f"Raw message: {raw}")
        raise ValueError("Impossible de trouver 'pubkey' dans le message WS")

    creation_ts = time.time()
    log.debug(f"Parsed token={token_address}, ts={creation_ts}")
    return token_address, creation_ts
