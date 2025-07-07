import asyncio
import json
import logging
import os
import time
from dotenv import load_dotenv

from utils.parser import parse_msg
from utils.honeypot import is_honeypot
from utils.liquidity import get_liquidity
from utils.scoring import score_token
from utils.tp_sl import monitor_token
from utils.jup_swap import buy_token
from utils.creator_tracker import (
    record_token_creation,
    is_suspicious,
    mark_token_as_rug,
)

load_dotenv()
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("main")

WS_URL = f"wss://mainnet.helius-rpc.com/?api-key={os.getenv('HELIUS_API_KEY')}"
SWAP_AMOUNT_LAMPORTS = int(float(os.getenv("SWAP_AMOUNT_SOL", "0.01")) * 1e9)


async def handle_new_token(token_address: str, timestamp: float, creator_wallet: str):
    log.info(f"👉 Nouveau token détecté : {token_address}")
    record_token_creation(creator_wallet, is_rug=False)

    try:
        honeypot = await is_honeypot(token_address, SWAP_AMOUNT_LAMPORTS)
    except Exception as e:
        log.error(f"{token_address}: ❌ Exception pendant is_honeypot: {e}")
        honeypot = True
    if honeypot:
        log.info(f"{token_address}: honeypot détecté, skip")
        return

    try:
        liquidity_ok = await get_liquidity(token_address)
    except Exception as e:
        log.error(f"{token_address}: ❌ Exception pendant check_liquidity: {e}")
        return
    if not liquidity_ok:
        log.info(f"{token_address}: liquidité insuffisante, skip")
        return

    score = score_token(token_address)
    log.info(f"{token_address}: Score = {score}")

    if is_suspicious(creator_wallet):
        log.warning(f"⚠️ Créateur {creator_wallet} suspect détecté, token {token_address}")

    try:
        buy_signature, amount_in, amount_out = await buy_token(token_address)
        log.info(f"✅ Achat effectué : {buy_signature}")
    except Exception as e:
        log.error(f"{token_address}: ❌ Erreur pendant l'achat: {e}")
        return

    await asyncio.sleep(3)
    try:
        await monitor_token(token_address, amount_in, amount_out, creator_wallet)
    except Exception as e:
        log.error(f"{token_address}: ❌ Erreur monitoring TP/SL: {e}")
        mark_token_as_rug(creator_wallet)


async def main():
    import websockets

    log.info("🚀 Démarrage du bot NONO")
    async with websockets.connect(WS_URL) as ws:
        log.info("✅ WS connecté")
        sub_msg = json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "programSubscribe",
            "params": [
                "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P",
                {"encoding": "jsonParsed", "filters": [{"dataSize": 165}]}
            ]
        })
        await ws.send(sub_msg)

        while True:
            raw = await ws.recv()
            try:
                token_address, timestamp = parse_msg(raw)
                creator_wallet = "DUMMY_CREATOR"  # à remplacer par vrai parsing si dispo
                await handle_new_token(token_address, timestamp, creator_wallet)
            except Exception as e:
                log.debug(f"WS non-notif: {raw}")
                continue


if __name__ == "__main__":
    asyncio.run(main())
