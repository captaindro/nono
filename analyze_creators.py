import json
import time
from datetime import datetime

STATS_PATH = "creator_stats.json"
THRESHOLD_RUGGED_COUNT = 3
THRESHOLD_RUGGED_RATIO = 0.5


def load_stats():
    with open(STATS_PATH, "r") as f:
        return json.load(f)


def analyze_creators():
    data = load_stats()
    print("📊 Analyse des créateurs de tokens\n")
    
    rows = []
    for wallet, stats in data.items():
        created = stats.get("created", 0)
        rugged = stats.get("rugged", 0)
        last_seen = stats.get("last_seen", None)
        ratio = rugged / created if created > 0 else 0
        trust_score = round((created - rugged) / created, 2) if created else 0

        flagged = (rugged >= THRESHOLD_RUGGED_COUNT) or (ratio >= THRESHOLD_RUGGED_RATIO)

        rows.append({
            "wallet": wallet,
            "created": created,
            "rugged": rugged,
            "ratio": round(ratio, 2),
            "trust_score": trust_score,
            "last_seen": datetime.fromtimestamp(last_seen).isoformat() if last_seen else "-",
            "🚨": "⚠️" if flagged else ""
        })

    rows.sort(key=lambda x: (-x["rugged"], x["trust_score"]))

    print(f"{'Wallet':<45} {'C':<3} {'R':<3} {'Rug%':<5} {'Score':<6} {'Last Seen':<20} 🚨")
    print("-" * 90)
    for row in rows:
        print(f"{row['wallet']:<45} {row['created']:<3} {row['rugged']:<3} {row['ratio']:<5} {row['trust_score']:<6} {row['last_seen']:<20} {row['🚨']}")


if __name__ == "__main__":
    analyze_creators()
