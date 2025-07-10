import asyncio
import websockets
import json
from utils.logger import get_logger

logger = get_logger(__name__)

HELIUS_WS_URL = "wss://mainnet.helius-rpc.com/?api-key=YOUR_API_KEY"

async def listen_helius(queue):
    """
    Écoute le WebSocket Helius pour les nouveaux tokens mintés.
    Place les données dans une queue asyncio pour traitement.
    """
    try:
        async with websockets.connect(HELIUS_WS_URL) as ws:
            logger.info("[helius] Connexion WebSocket établie")
            await ws.send(json.dumps({
                "jsonrpc": "2.0",
                "id": 1,
                "method": "programSubscribe",
                "params": {
                    "programId": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
                    "encoding": "jsonParsed"
                }
            }))
            while True:
                msg = await ws.recv()
                data = json.loads(msg)
                # Extraction et filtrage simplifié
                if 'method' in data and data['method'] == 'programNotification':
                    mint_info = data['params']['result']['value']['mint']
                    logger.debug(f"[helius] Nouveau mint détecté: {mint_info}")
                    await queue.put(mint_info)
    except Exception as e:
        logger.error(f"[helius] Erreur WebSocket: {e}")
        # Reconnexion après délai
        await asyncio.sleep(5)
        await listen_helius(queue)
