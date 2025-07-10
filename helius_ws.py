import asyncio
import logging
import websockets
import json
import os

from utils.jup_swap import execute_swap  # adapte le chemin si besoin

logger = logging.getLogger("helius_ws")

HEL_API_KEY = os.getenv("HEL_API_KEY")
HEL_WS_URL = f"wss://mainnet.helius-rpc.com/?api-key={HEL_API_KEY}"

# Paramètres personnalisables
BUY_AMOUNT_SOL = 0.01  # montant à acheter en SOL (à adapter)

async def handle_message(message):
    try:
        data = json.loads(message)
        logger.info(f"Message reçu: {data}")

        # Exemple simple de filtre : on cherche un mint Pump.fun
        # A adapter à ta structure exacte de message Helius / Pump.fun
        if "mint" in data:
            token_address = data["mint"]
            logger.info(f"Token mint détecté : {token_address}, lancement achat...")

            # Appel à ta fonction d'achat (async ou sync ? ici sync)
            # Si execute_swap est async, ajoute await
            result = execute_swap(token_address, BUY_AMOUNT_SOL)
            logger.info(f"Achat lancé pour {token_address}, résultat : {result}")

    except Exception as e:
        logger.error(f"Erreur traitement message WS : {e}")

async def start_helius_ws():
    while True:
        try:
            async with websockets.connect(HEL_WS_URL, ping_interval=20, ping_timeout=10) as ws:
                logger.info("Connexion WebSocket Helius établie")
                async for message in ws:
                    await handle_message(message)
        except websockets.exceptions.ConnectionClosedError as e:
            logger.warning(f"WS fermée, reconnexion : {e}")
        except Exception as e:
            logger.error(f"Erreur WebSocket Helius : {e}")
        await asyncio.sleep(5)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(start_helius_ws())
