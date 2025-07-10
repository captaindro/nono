import csv
import os
from datetime import datetime
from utils.config import CSV_OUTPUT_PATH

FIELDNAMES = ["timestamp", "token_address", "profit_lamports", "wallet_pubkey"]

def log_successful_trade(token_address: str, profit_lamports: int, wallet_pubkey: str):
    """
    Enregistre une vente réussie dans un fichier CSV.
    """
    try:
        os.makedirs(os.path.dirname(CSV_OUTPUT_PATH), exist_ok=True)

        file_exists = os.path.isfile(CSV_OUTPUT_PATH)
        with open(CSV_OUTPUT_PATH, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)

            if not file_exists:
                writer.writeheader()

            writer.writerow({
                "timestamp": datetime.utcnow().isoformat(),
                "token_address": token_address,
                "profit_lamports": profit_lamports,
                "wallet_pubkey": wallet_pubkey
            })

    except Exception as e:
        print(f"[CSV Logger] Erreur lors de l'enregistrement du trade : {e}")
