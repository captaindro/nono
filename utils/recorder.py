# utils/recorder.py

import csv
import logging
from datetime import datetime
from pathlib import Path

CSV_FILE = Path("trades_success.csv")
logger = logging.getLogger("utils.recorder")

def record_success(
    token_address: str,
    token_symbol: str,
    gain_lamports: int,
    amount_in: int,
    amount_out: int,
    buy_signature: str,
    sell_signature: str
):
    gain_sol = gain_lamports / 1_000_000_000
    gain_pct = (gain_lamports / amount_in) * 100 if amount_in > 0 else 0

    write_header = not CSV_FILE.exists()

    try:
        with open(CSV_FILE, mode="a", newline="") as file:
            writer = csv.writer(file)
            if write_header:
                writer.writerow([
                    "horodatage",
                    "adresse_token",
                    "symbole_token",
                    "gain_lamports",
                    "gain_en_SOL",
                    "gain_en_pourcentage",
                    "montant_acheté_lamports",
                    "montant_revendu_lamports",
                    "signature_achat",
                    "signature_vente"
                ])
            writer.writerow([
                datetime.utcnow().isoformat(),
                token_address,
                token_symbol,
                gain_lamports,
                gain_sol,
                gain_pct,
                amount_in,
                amount_out,
                buy_signature,
                sell_signature
            ])
        logger.info(
            f"[CSV] ✅ {token_symbol} | Gain: {gain_sol:.4f} SOL ({gain_pct:.2f}%) | Buy: {buy_signature[:6]}... | Sell: {sell_signature[:6]}..."
        )
    except Exception as e:
        logger.exception(f"[CSV] ❌ Erreur lors de l'enregistrement du trade : {e}")
