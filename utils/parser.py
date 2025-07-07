import json
import logging

log = logging.getLogger("nono.parser")

def parse_msg(raw_msg: str):
    msg = json.loads(raw_msg)

    # Si le message n'est pas une notification utile
    if "method" in msg and msg["method"] != "accountNotification":
        return None, None

    try:
        # ✅ Donnée complète pour Pump.fun (mint réel)
        mint = msg["params"]["result"]["value"]["data"]["parsed"]["info"]["mint"]
        slot = msg["params"]["result"]["context"]["slot"]
        return mint, slot

    except KeyError:
        try:
            # ✅ Si donnée partielle, on prend pubkey brut
            mint = msg["params"]["result"]["value"]["pubkey"]
            return mint, None
        except KeyError:
            raise ValueError("Impossible de trouver 'pubkey'")
