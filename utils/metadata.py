import os
import httpx
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger("metadata")

RPC_URL_MAINNET = os.getenv("RPC_URL_MAINNET")

async def get_token_creator(token_address: str) -> str:
    """
    Récupère le wallet du créateur d’un token minté sur Pump.fun
    """
    if not RPC_URL_MAINNET:
        logger.error("RPC_URL_MAINNET manquant dans le .env.")
        return None

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getAccountInfo",
        "params": [
            token_address,
            {
                "encoding": "jsonParsed",
                "commitment": "confirmed"
            }
        ]
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(RPC_URL_MAINNET, json=payload)
            result = response.json()["result"]
            if not result or not result.get("value"):
                return None

            creator = result["value"]["data"]["parsed"]["info"]["mintAuthority"]
            return creator
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du creator : {e}", exc_info=True)
        return None


async def fetch_token_metadata(token_address: str) -> dict:
    """
    Récupère les métadonnées du token (name, symbol, etc.) via Helius getTokenMetadata
    """
    if not RPC_URL_MAINNET:
        logger.error("RPC_URL_MAINNET manquant.")
        return {}

    url = f"{RPC_URL_MAINNET}"
    helius_url = url.split("?")[0] + "/v0/token-metadata?api-key=" + os.getenv("HEL_API_KEY")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{helius_url}&mint={token_address}")
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                return data[0]
            elif isinstance(data, dict):
                return data
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du token metadata : {e}", exc_info=True)

    return {}
