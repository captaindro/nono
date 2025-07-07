import json

def parse_msg(raw_msg: str):
    msg = json.loads(raw_msg)

    # 🚫 Si c'est une réponse générique ou pas une notif Pump.fun
    if "method" in msg and msg["method"] != "accountNotification":
        return None, None

    # 🚫 Si result est null (ex: {"result": null})
    if not msg.get("params") or not msg["params"].get("result"):
        return None, None

    try:
        # ✅ Cas classique Pump.fun (mint réel et complet)
        mint = msg["params"]["result"]["value"]["data"]["parsed"]["info"]["mint"]
        slot = msg["params"]["result"]["context"]["slot"]
        return mint, slot

    except KeyError:
        try:
            # ✅ Cas partiel : on utilise seulement pubkey
            mint = msg["params"]["result"]["value"]["pubkey"]
            return mint, None
        except KeyError:
            raise ValueError("Impossible de trouver 'pubkey'")
