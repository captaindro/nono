# utils/liquidity.py

import os
from solana.rpc.api import Client

# ───────────────────────────────────────────────────────────────────────────────
# MAPPING DES POOLS RAYDIUM SOL–TOKEN (Mainnet)
#
# Adresses de compte de liquidité SOL–<token> pour chaque token mint ciblé.
# Vous pouvez ajouter d’autres mappages ici si besoin.
# ───────────────────────────────────────────────────────────────────────────────
POOL_MAP = {
    # SOL / USDC
    "So11111111111111111111111111111111111111112": "58oQChx4yWmvKdwLLZzBi4ChoCc2fqCUWBkwMihLYQo2",  # SOL/USDC pool :contentReference[oaicite:0]{index=0}

    # USDC / SOL (même pool, clé côté USDC mint)
    "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v": "3gSjs6MqyHFsp8DXvaKvVUJjV7qg5itf9qmUGuhnSaWH",  # USDC/SOL pool :contentReference[oaicite:1]{index=1}

    # SOL / USDT
    "Es9vMFrzaCERQ5Bd4HL81miEamUHUSYs8Dualy3QF57S": "7XawhbbxtsRcQA8KTkHT9f9nc6d69UwqCDh6U5EEbEmX",  # SOL/USDT pool :contentReference[oaicite:2]{index=2}
}

# Initialisation du client RPC Solana
RPC = Client(os.getenv("RPC_URL"))

def get_liquidity(token_mint: str) -> float:
    """
    Vérifie la liquidité SOL disponible dans le pool Raydium pour `token_mint`.
    Retourne la quantité de SOL (float). Si le mint n'est pas mappé, retourne 0.0.
    """
    pool_account = POOL_MAP.get(token_mint)
    if not pool_account:
        return 0.0

    resp = RPC.get_account_info(pool_account, encoding="jsonParsed")
    value = resp.get('result', {}).get('value')
    if not value:
        return 0.0

    lamports = value.get('lamports', 0)
    return lamports / 1e9
