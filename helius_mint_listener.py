# helius_mint_listener.py

import asyncio
import json
import logging
import websockets

from config.settings import settings
# from utils.filters.token_passes_filters import token_passes_filters

logger = logging.getLogger("mint_listener")


async def listen_for_mint_tokens(callback):
    """
    Écoute les mints via WebSocket Helius.
    Appelle callback(token_address, creator_address) à chaque mint détecté.
    """
    ws_url = settings.ws_helius
    program_id = settings.pumpfun_program_id

    while True:
        try:
            async with websockets.connect(ws_url) as ws:
                logger.info("🟢 Connexion WS Helius établie.")
                sub = {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "logsSubscribe",
                    "params": [{"mentions": [program_id]}, {"commitment": "processed"}]
                }
                await ws.send(json.dumps(sub))
                logger.info("📡 Abonnement logs envoyé.")

                async for msg in ws:
                    logger.debug(f"[WS RAW] {msg}")
                    data = json.loads(msg)
                    params = data.get("params", {}).get("result", {})
                    logs = params.get("logs", [])
                    sig = params.get("signature", "")

                    for line in logs:
                        if "Instruction: CreateToken" in line:
                            creator = extract_address(logs, "creator: ")
                            mint = extract_address(logs, "mint: ")
                            if not mint or not creator:
                                logger.warning(f"⚠️ Impossible d’extraire mint/creator de {logs}")
                                continue
                            logger.info(f"🪙 Mint détecté : {mint} by {creator} (sig {sig})")
                            await callback(token_address=mint, creator_address=creator)

        except websockets.exceptions.ConnectionClosed:
            logger.warning("🔁 WS fermée, reconnexion dans 3s…")
            await asyncio.sleep(3)

        except Exception as e:
            logger.error(f"❌ Erreur WS Helius: {e}", exc_info=True)
            await asyncio.sleep(5)


def extract_address(logs: list[str], prefix: str) -> str | None:
    """Extrait l’adresse qui suit un préfixe dans la liste de logs."""
    for l in logs:
        if prefix in l:
            return l.split(prefix, 1)[1].strip()
    return None


if __name__ == "__main__":
    # Test rapide du WS
    async def cb(mint, creator):
        print("Callback:", mint, creator)
    asyncio.run(listen_for_mint_tokens(cb))
