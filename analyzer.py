import requests

def extract_token_address(notification_data):
    try:
        account_data = notification_data["params"]["result"]["value"]
        token_address = account_data["pubkey"]
        return token_address
    except Exception as e:
        print(f"[ERREUR extraction mint] {e}")
        return None

def is_honeypot(token_address):
    # ⚠️ À remplacer par un vrai honeypot checker (API ou simulation)
    return False  # Pour le moment on suppose que ce n'est pas un honeypot

def has_sufficient_liquidity(token_address):
    # ⚠️ À remplacer par une vérification réelle (via API Jupiter ou RPC)
    return True  # On considère pour le test qu'il y a assez de liquidité

def score_token(token_address):
    score = 0

    if not is_honeypot(token_address):
        score += 1
    if has_sufficient_liquidity(token_address):
        score += 1

    # D'autres critères peuvent être ajoutés ici
    return score
