# utils/parser.py

import json

def parse_msg(msg: str) -> dict:
    """
    Parse la chaîne JSON reçue du WebSocket Helius Pump.fun
    et extrait l'adresse du token mint.
    Retourne un dict {'mint': <str>, ...} pour traitement ultérieur.
    """
    data = json.loads(msg)
    # Exemple de structure attendue :
    # {
    #   "method": "accountNotification",
    #   "params": {
    #       "result": {
    #           "context": {...},
    #           "value": {
    #               "pubkey": "<adresse_du_compte>",
    #               "account": {
    #                   "data": [...],
    #                   "executable": false,
    #                   "lamports": ...,
    #                   "owner": "<programme_pump.fun>",
    #                   "rentEpoch": ...
    #               }
    #           }
    #       }
    #   }
    # }
    params = data.get("params", {})
    result = params.get("result", {})
    value = result.get("value", {})
    # Si le mint est dans account.data, il faut le décoder selon le layout SPL Token
    # Ici on suppose que la 'pubkey' correspond directement au mint du token
    mint = value.get("pubkey")
    return {"mint": mint}
