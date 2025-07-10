import logging
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

RPC_URL = os.getenv("RPC_URL_MAINNET")

PUMPFUN_PROGRAM_ID = os.getenv("PUMPFUN_PROGRAM_ID")

logger = logging.getLogger("program_id_checker")


async def check_program_id():
    """
    Vérifie dynamiquement le dernier programme actif PumpBoard pour récupérer son programId.
    """
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getSignaturesForAddress",
            "params": [
                PUMPFUN_PROGRAM_ID,
                {"limit": 1}
            ]
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(RPC_URL, json=payload)

        if response.status_code == 200:
            data = response.json()
            if "result" in data and len(data["result"]) > 0:
                logger.info("Program ID actif vérifié depuis la dernière signature PumpBoard.")
                return PUMPFUN_PROGRAM_ID
            else:
                logger.warning("Aucune signature trouvée pour PumpBoard.")
                return None
        else:
            logger.error(f"Erreur HTTP RPC ({response.status_code}) : {response.text}")
            return None

    except Exception as e:
        logger.error(f"Erreur dans check_program_id : {e}", exc_info=True)
        return None
