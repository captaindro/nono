# utils/transaction_logger.py

import csv
import os
from datetime import datetime
from utils.logger import get_logger

logger = get_logger(__name__)

CSV_FILE = "transactions.csv"

def log_transaction(token_name, token_address, amount_gained):
    """
    Enregistre une transaction profitable dans un fichier CSV.
    """
    try:
        file_exists = os.path.isfile(CSV_FILE)
        with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['timestamp', 'token_name', 'token_address', 'amount_gained']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            writer.writerow({
                'timestamp': datetime.utcnow().isoformat(),
                'token_name': token_name,
                'token_address': token_address,
                'amount_gained': amount_gained
            })

        logger.info(f"[transaction_logger] Transaction loggée pour {token_name} ({amount_gained} SOL)")
    except Exception as e:
        logger.error(f"[transaction_logger] Erreur d’écriture CSV : {e}")
