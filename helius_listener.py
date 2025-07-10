import asyncio
import json
import logging
import websockets
from dotenv import load_dotenv
import os

load_dotenv()

HEL_API_KEY = os.getenv("HEL_API_KEY")
WS_HELIUS_URL = f"wss://rpc.helius.xyz/?api-key={HEL_API_KEY}"

logger = logging.getLogger("helius_listener")


async def start_helius_ws(callback, program_id):
    """
    Écoute les nouveaux events sur le programme Pump.fun via WebSocket Helius.
    Le paramètre `program_id` permet de cibler dynamiquement un programme spécifique.
    """
    logger.info(f"Connexion au WebSocket Helius... Program ID écouté : {program_id}")
    try:
        async with websockets.connect(WS_HELIUS_URL) as ws:
            subscription = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "programSubscribe",
                "params": [
                    program_id,
                    {
                        "commitment": "processed",
                        "encoding": "base64"
                    }
                ]
            }

            await ws.send(json.dumps(subscription))
            logger.info("Souscription envoyée à Helius WebSocket.")

            while True:
                message = await ws.recv()
                data = json.loads(message)

                if "params" in data and "result" in data["params"]:
                    await callback(data["params"]["result"])

    except Exception as e:
        logger.error(f"Erreur dans le WebSocket Helius : {e}", exc_info=True)
        await asyncio.sleep(5)
        await start_helius_ws(callback, program_id)  # Retry automatique en cas d’erreur
