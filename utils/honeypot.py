import os
import requests

JUPITER_SIM_URL = "https://quote-api.jup.ag/v4/swap/simulate"

def is_honeypot(token_mint: str, amount: int, slippage_bps: int = 50) -> bool:
    payload = {
        "mintIn": token_mint,
        "mintOut": "So11111111111111111111111111111111111111112",
        "amount": amount,
        "slippageBps": slippage_bps,
        "userPublicKey": os.getenv("YOUR_PUBLIC_KEY")
    }
    try:
        resp = requests.get(JUPITER_SIM_URL, params=payload, timeout=5)
        data = resp.json()
    except:
        return True

    success = data.get("success", False)
    out_amount = data.get("data", {}).get("outAmount", 0)
    return not success or out_amount <= 0