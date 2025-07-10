from solana.rpc.async_api import AsyncClient
import logging

logger = logging.getLogger(__name__)

async def get_tx_creator(rpc_url: str, signature: str) -> str | None:
    async with AsyncClient(rpc_url) as client:
        resp = await client.get_transaction(signature)
        if not resp['result']:
            logger.warning(f"Transaction {signature} introuvable")
            return None

        tx = resp['result']['transaction']
        message = tx['message']

        # Liste des comptes signataires
        account_keys = message.get('accountKeys', [])
        if not account_keys:
            logger.warning(f"Aucun accountKeys dans tx {signature}")
            return None

        # Le premier signer est souvent le créateur
        creator = account_keys[0]
        return creator
