# utils/parser.py

import json

def parse_msg(raw_msg: str):
    msg = json.loads(raw_msg)

    # Cas des réponses internes ("result") => ignorer
    if "result" in msg:
        return None, None

    try:
        mint = msg["params"]["result"]["value"]["data"]["parsed"]["info"]["mint"]
        timestamp = msg["params"]["result"]["context"]["slot"]
        return mint, timestamp
    except KeyError:
        try:
            # Fallback si pas de data structuré : tenter d'extraire "pubkey" (ex: test simple)
            mint = msg["params"]["result"]["value"]["pubkey"]
            return mint, None
        except KeyError:
            raise ValueError("Impossible de trouver 'pubkey' ou 'data' dans le message")

