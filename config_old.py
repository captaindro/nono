# settings.py

import os
from dotenv import load_dotenv

load_dotenv()

config = {
    "quote_amount": int(os.getenv("QUOTE_AMOUNT", "10000000")),  # 0.01 SOL par défaut
    "slippage_bps": int(os.getenv("SLIPPAGE_BPS", "50")),
    "token_score_threshold": int(os.getenv("TOKEN_SCORE_THRESHOLD", "50")),
    "simulate_only": os.getenv("SIMULATE_ONLY", "false").lower() == "true",
}
