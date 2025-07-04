import json
from pathlib import Path

SCORES_FILE = Path("wallets/wallet_scores.json")

def load_scores():
    if SCORES_FILE.exists():
        with open(SCORES_FILE, "r") as f:
            return json.load(f)
    return {}

def save_scores(scores):
    with open(SCORES_FILE, "w") as f:
        json.dump(scores, f, indent=2)

def update_wallet_score(wallet, change):
    scores = load_scores()
    scores[wallet] = scores.get(wallet, 0) + change
    save_scores(scores)

def get_top_wallets(threshold=5):
    scores = load_scores()
    return [wallet for wallet, score in scores.items() if score >= threshold]

def is_blacklisted(wallet):
    scores = load_scores()
    return scores.get(wallet, 0) < 0
