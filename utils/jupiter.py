# utils/jupiter.py

import os
import asyncio
import logging
import httpx
from solana.rpc.async_api import AsyncClient
from solana.transaction import Transaction
from solana.publickey import PublicKey

log = logging.getLogger("nono.jupiter")

JUPITER_API = os.getenv("JUPITER_API_URL", "https://quote-api.jup.ag")
RPC_URL     = os.getenv("RPC_URL_MAINNET")  # ou RPC_URL_DEVNET selon ENV

async def execute_swap(
    wallet_pubkey: str,
    wallet_signer,          # Keypair de solana-py
    input_mint: str,         # SOL mint: "So1111…"
    output_mint: str,        # token à sniper
    amount: int,             # montant en lamports SOL (1 SOL = 1e9 lamports)
    slippage_bps: int = 50
) -> bool:
    """
    1. Récupère une quote depuis Jupiter
    2. Construit la transaction
    3. La signe et l'envoie
    Retourne True si confirmé, False sinon.
    """
    client = AsyncClient(RPC_URL)
    async with client:
        # 1️⃣ get quote
        params = {
            "inputMint": input_mint,
            "outputMint": output_mint,
            "amount": str(amount),
            "slippageBps": str(slippage_bps),
            "feeBps": "0"
        }
        try:
            res = httpx.get(f"{JUPITER_API}/v4/quote", params=params, timeout=10).json()
        except Exception as e:
            log.error(f"Jupiter quote error: {e}")
            return False

        routes = res.get("data")
        if not routes:
            log.error("Jupiter: pas de route trouvée")
            return False
        route = routes[0]

        # 2️⃣ build transaction
        try:
            swap_tx = httpx.post(
                f"{JUPITER_API}/v4/swap",
                json={"route": route, "userPublicKey": wallet_pubkey},
                timeout=10
            ).json()
        except Exception as e:
            log.error(f"Jupiter swap error: {e}")
            return False

        encoded = swap_tx.get("swapTransaction")
        if not encoded:
            log.error("Jupiter: pas de swapTransaction")
            return False

        # 3️⃣ send
        import base64
        raw = base64.b64decode(encoded)
        tx = Transaction.deserialize(raw)
        try:
            sig = await client.send_raw_transaction(tx.serialize(), opts={"skipPreflight": False})
            confirmed = await client.confirm_transaction(sig.value)
        except Exception as e:
            log.error(f"Erreur envoi transaction: {e}")
            return False

        if confirmed.value.err:
            log.error(f"Swap échoué: {confirmed.value.err}")
            return False

        log.info(f"Swap réussi, signature: {sig.value}")
        return True
