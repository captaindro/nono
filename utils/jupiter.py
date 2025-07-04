# utils/jupiter.py

import os
import base64
import requests
from solana.rpc.api import Client
from solana.transaction import Transaction
from solana.account import Account

# Endpoints Jupiter
JUPITER_QUOTE_URL = "https://quote-api.jup.ag/v4/quote"
JUPITER_SWAP_URL  = "https://quote-api.jup.ag/v4/swap"

# Client Solana RPC
RPC = Client(os.getenv("RPC_URL"))

def get_swap_route(input_mint: str, output_mint: str, amount: int, slippage_bps: int):
    """
    Récupère la transaction de swap (base64) et le montant attendu en sortie.
    """
    params = {
        "inputMint": input_mint,
        "outputMint": output_mint,
        "amount": amount,
        "slippageBps": slippage_bps,
    }
    res = requests.get(JUPITER_QUOTE_URL, params=params, timeout=5)
    res.raise_for_status()
    data = res.json().get("data", [])
    if not data:
        raise RuntimeError("Aucune route de swap trouvée")
    route = data[0]
    return route["swapTransaction"], route["outAmount"]

def execute_swap(input_mint: str,
                 output_mint: str,
                 amount: int,
                 slippage_bps: int):
    """
    Exécute un swap via Jupiter :
      1. Récupère la tx raw (base64)
      2. Désérialise, signe et envoie via solana-py
    Retourne (signature, montant_attendu).
    """
    raw_tx_b64, expected_out = get_swap_route(
        input_mint, output_mint, amount, slippage_bps
    )
    raw_tx = base64.b64decode(raw_tx_b64)

    # Charger et signer le wallet
    wallet_path = os.getenv("WALLET_PATH")
    with open(wallet_path, "r") as f:
        keypair_json = f.read()
    acct = Account.from_json(keypair_json)

    tx = Transaction.deserialize(raw_tx)
    tx.sign(acct)

    # Envoi
    resp = RPC.send_raw_transaction(
        tx.serialize(),
        opts={"skip_preflight": False, "preflight_commitment": "confirmed"}
    )
    return resp, expected_out
