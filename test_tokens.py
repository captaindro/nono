import requests
import json

def test_api(url, name):
    print(f"--- Test API {name} ---")
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        print(json.dumps(data, indent=2)[:1000])  # Affiche les 1000 premiers caractères pour éviter trop gros output
        # Si tu veux, tu peux ajouter des vérifications spécifiques ici
    except Exception as e:
        print(f"Erreur lors de la requête sur {name} : {e}")

if __name__ == "__main__":
    apis = {
        "Dexscreener": "https://api.dexscreener.com/latest/dex/tokens/solana",
        "Solscan": "https://public-api.solscan.io/token/creation",
        "StepFinance": "https://api.step.finance/api/tokens/recent"  # Hypothétique, à confirmer
    }

    for name, url in apis.items():
        test_api(url, name)
        print("\n")
