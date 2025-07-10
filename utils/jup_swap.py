<<<<<<< HEAD
import logging
import asyncio

log = logging.getLogger(__name__)

async def buy_token(mint_address: str, amount_sol: float) -> str:
    log.info(f"🛒 Achat simulé de {amount_sol} SOL sur le token {mint_address}")
    await asyncio.sleep(1)
    return f"fake-buy-txid-{mint_address}"

async def sell_token(mint: str, amount: float):
    log.info(f"💰 Vente simulée de {amount} {mint}")
    await asyncio.sleep(1)
    return True
=======
# utils/jup_swap.py

import base64
import json
import httpx
from typing import Optional, Literal

from loguru import logger
from solders.keypair import Keypair
from solders.transaction import VersionedTransaction
from solana.rpc.async_api import AsyncClient
from solana.rpc.types import TxOpts

from config.settings import settings


async def execute_swap(
    amount: int,
    input_mint: str,
    output_mint: str,
    wallet_path: Optional[str] = None,
    wallet: Optional[Keypair] = None,
    token_address: Optional[str] = None,
    simulate_only: bool = False,
    side: Literal["buy", "sell"] = "buy",
) -> Optional[dict]:
    """
    Exécute un swap via Jupiter API :
      1) GET /v6/quote (fallback GET /quote si nécessaire)
      2) POST /v6/swap

    Args:
        amount: montant en lamports (1 SOL = 1e9 lamports)
        input_mint: mint de l’actif d’entrée (SOL mint pour SOL natif)
        output_mint: mint du token cible
        wallet_path: chemin vers JSON du wallet (Keypair)
        wallet: Keypair déjà chargé (prioritaire)
        token_address: adresse du token pour retour/CSV
        simulate_only: si True, ne broadcast pas la tx
        side: "buy" ou "sell" pour le log

    Returns:
        dict ou None :
          - Simulation : {"simulation": True, "tx": VersionedTransaction}
          - Réel       : {"tx_signature": str, "token": token_address}
    """
    try:
        # --- Charger le wallet ---
        if wallet is None:
            if not wallet_path:
                raise ValueError("Vous devez fournir wallet ou wallet_path.")
            with open(wallet_path, "r") as f:
                secret = json.load(f)
            wallet = Keypair.from_bytes(bytes(secret))

        user_pub = str(wallet.pubkey())
        base_url = settings.jupiter_api_url.rstrip("/")

        # --- 1) Quote (GET /v6/quote, fallback /quote) ---
        params = {
            "amount": str(amount),
            "inputMint": input_mint,
            "outputMint": output_mint,
            "slippageBps": settings.slippage_bps,
            "onlyDirectRoutes": settings.jupiter_only_direct_routes,
            "userPublicKey": user_pub,
        }

        quote_url_v6 = f"{base_url}/v6/quote"
        logger.debug(f"[JUPITER] GET {quote_url_v6} params: {params}")
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(quote_url_v6, params=params)

            # fallback si v6/quote indisponible ou 400/405
            if resp.status_code in (400, 405):
                quote_url_alt = f"{base_url}/quote"
                logger.warning(f"[JUPITER] Fallback quote sur /quote (code {resp.status_code})")
                resp = await client.get(quote_url_alt, params=params)

        if resp.status_code != 200:
            logger.error(f"[JUPITER] Erreur HTTP {resp.status_code} sur quote\n{resp.text}")
            return None

        quote_data = resp.json()
        if settings.expert_mode:
            logger.debug(f"[JUPITER] Raw quote response:\n{json.dumps(quote_data, indent=2)}")

        # --- 2) Swap (POST /v6/swap) ---
        swap_url = f"{base_url}/v6/swap"
        swap_payload = {
            "quoteResponse": quote_data,
            "userPublicKey": user_pub,
            "wrapUnwrapSOL": True,
            "slippageBps": settings.slippage_bps,
            "onlyDirectRoutes": settings.jupiter_only_direct_routes,
        }
        logger.debug(f"[JUPITER] POST {swap_url} payload keys: {list(swap_payload.keys())}")

        async with httpx.AsyncClient(timeout=15) as client:
            swap_resp = await client.post(swap_url, json=swap_payload)

        if swap_resp.status_code != 200:
            logger.error(f"[JUPITER] Erreur HTTP {swap_resp.status_code} sur swap\n{swap_resp.text}")
            return None

        swap_data = swap_resp.json()
        if settings.expert_mode:
            logger.debug(f"[JUPITER] Raw swap response:\n{json.dumps(swap_data, indent=2)}")

        tx_b64 = swap_data.get("swapTransaction")
        if not tx_b64:
            logger.warning("[JUPITER] Aucune transaction retournée pour le swap.")
            return None

        # --- Signer la transaction ---
        tx = VersionedTransaction.from_bytes(base64.b64decode(tx_b64))
        tx = tx.sign([wallet])

        if simulate_only:
            logger.info("[SWAP] Simulation uniquement, tx non envoyée.")
            return {"simulation": True, "tx": tx}

        # --- Broadcast via Helius RPC ---
        async with AsyncClient(settings.rpc_helius) as sol_client:
            resp_send = await sol_client.send_raw_transaction(
                tx.serialize(),
                opts=TxOpts(skip_preflight=True, preflight_commitment="processed"),
            )

        signature = resp_send.value
        logger.success(f"[SWAP {side.upper()}] Transaction envoyée: {signature}")
        return {"tx_signature": signature, "token": token_address}

    except Exception as e:
        logger.exception(f"[JUPITER] Erreur dans execute_swap ({side.upper()}): {e}")
        return None
>>>>>>> 2553739 (Ajout de la config Railway et du workflow CI/CD)
