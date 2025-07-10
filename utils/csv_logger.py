import os
import csv
from datetime import datetime
from config.settings import settings
from loguru import logger as log


def log_transaction_csv(token_address: str, profit_amount: float, wallet_used: str, origin_tx: str, swap_tx: str, sell: bool = False):
    """
    Log une transaction (achat ou vente) dans le fichier CSV défini.
    """
    if not settings.CSV_OUTPUT_ENABLED:
        return

    file_path = settings.CSV_OUTPUT_PATH
    is_new_file = not os.path.exists(file_path)

    try:
        with open(file_path, mode='a', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            if is_new_file:
                writer.writerow(["timestamp", "token", "wallet", "origin_tx", "swap_tx", "profit", "type"])

            writer.writerow([
                datetime.utcnow().isoformat(),
                token_address,
                wallet_used,
                origin_tx or "",
                swap_tx or "",
                profit_amount if profit_amount is not None else "",
                "SELL" if sell else "BUY"
            ])
        log.info(f"[CSV] Transaction {'SELL' if sell else 'BUY'} loggée pour {token_address}")
    except Exception as e:
        log.exception(f"[CSV] ❌ Erreur écriture CSV : {e}")
