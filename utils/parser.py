# utils/parser.py

import json
import time
import logging

log = logging.getLogger("nono.parser")

def parse_msg(raw: str) -> tuple[str, float]:
    """
    Parse un message JSON reçu du WebSocket Helius Pump.fun.

    Gère à la fois :
     - getProgramAccounts → {"jsonrpc":"2.0","id":...,"result":[{...}, ...]}
     - subscription       → {"jsonrpc":"2.0","method":"accountNotification","params":{"result":{...},"subscription":...}}

    Retourne (token_address, receipt_timestamp).
    """
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON invalide: {e}")

    # Cas 1 : result est une liste (RPC WS getProgramAccounts)
    if isinstance(data.get("result"), list):
        lst = data["result"]
        if not lst:
            raise ValueError("Liste 'result' vide")
        first = lst[0]
        token_address = first.get("pubkey")
        if not token_address:
            raise ValueError("Pas de 'pubkey' dans result[0]")
    # Cas 2 : subscription (accountNotification)
    elif "params" in data and isinstance(data["params"].get("result"), dict):
        res = data["params"]["result"]
        token_address = res.get("pubkey") or res.get("account", {}).get("owner")  # owner fallback
        if not token_address:
            raise ValueError("Pas de 'pubkey' dans params.result")
    else:
        raise ValueError("Format de message WS inattendu")

    creation_ts = time.time()
    log.debug(f"Parsed token={token_address}, ts={creation_ts}")
    return token_address, creation_ts
