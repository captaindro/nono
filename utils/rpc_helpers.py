# utils/rpc_helpers.py
import httpx
import logging

logger = logging.getLogger(__name__)

async def get_tx_creator(rpc_url: str, signature: str) -> str | None:
    """
    Récupère l'adresse du créateur (premier signer) d'une transaction Solana via son signature.

    Args:
        rpc_url: URL RPC Solana (ex: https://api.mainnet-beta.solana.com)
        signature: Signature de la transaction (str)

    Returns:
        str: adresse du créateur (premier signer) ou None si erreur.
    """
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTransaction",
        "params": [signature, {"encoding": "jsonParsed"}]
    }

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(rpc_url, json=payload)
            response.raise_for_status()
            data = response.json()

        tx = data.get("result")
        if not tx:
            logger.warning(f"Transaction introuvable ou non confirmée: {signature}")
            return None

        # On récupère la première clé signataire (créateur)
        message = tx.get("transaction", {}).get("message", {})
        account_keys = message.get("accountKeys", [])
        if not account_keys:
            logger.warning(f"Pas de clés accountKeys trouvées pour tx: {signature}")
            return None

        # Chaque élément de accountKeys est un dict avec 'pubkey' et 'signer'
        # On cherche la première clé qui est signataire
        for acc in account_keys:
            if acc.get("signer", False):
                return acc.get("pubkey")

        logger.warning(f"Aucun signataire trouvé pour tx: {signature}")
        return None

    except Exception as e:
        logger.error(f"Erreur get_tx_creator pour tx {signature}: {e}")
        return None
