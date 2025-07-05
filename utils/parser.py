# utils/parser.py

import json
import time
import logging

log = logging.getLogger("nono.parser")

def parse_msg(raw: str) -> tuple[str, float]:
    """
    Parse un message JSON reçu du WebSocket Helius Pump.fun.

    raw: chaîne JSON
    Retourne (token_address, creation_timestamp).

    Si le format n'est pas celui attendu, lève une exception.
    """
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON invalide: {e}")

    # Selon l'API Helius, le payload peut être dans "result" direct ou sous "params"
    result = data.get("result") or data.get("params", {}).get("result")
    if not result or not isinstance(result, list):
        raise ValueError("Résultat inattendu, pas de liste 'result'")

    # On prend le premier compte créé (généralement unique)
    first = result[0]
    token_address = first.get("pubkey")
    if not token_address:
        raise ValueError("Pas de champ 'pubkey' dans le message")

    # timestamp à l'instant de réception
    creation_ts = time.time()
    log.debug(f"Parsed token={token_address}, ts={creation_ts}")
    return token_address, creation_ts
