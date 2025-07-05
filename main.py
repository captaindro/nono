#!/usr/bin/env python3
import os
import time
import asyncio
import logging
import subprocess
import requests

from solana.rpc.async_api import AsyncClient
from solana.publickey import PublicKey

from utils.parser import parse_msg
from utils.honeypot import is_honeypot
from utils.liquidity import get_liquidity
from utils.tp_sl import calculate_tp_sl
from utils.scoring import score_token

# Paramètres dynamiques depuis env
TP_MULTIPLIER = float(os.getenv("take_profit_multiplier", 1.1))
SL_MULTIPLIER = float(os.getenv("stop_loss_multiplier", 0.8))
SLIPPAGE_BPS  = int(os.getenv("slippage_bps", 50))
LIQ_THRESH    = float(os.getenv("liquidity_threshold_sol", 0.5))
SCORE_THRESH  = float(os.getenv("token_score_threshold", 0.7))

# Configuration Helius
RPC_URL = os.getenv("RPC_URL_MAINNET") if os.getenv("ENVIRONMENT") == "mainnet" else os.getenv("RPC_URL_DEVNET")
WS_URL  = os.getenv("WS_URL_MAINNET")  if os.getenv("ENVIRONMENT") == "mainnet" else os.getenv("WS_URL_DEVNET")
API_KEY = os.getenv("HEL_API_KEY")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("nono")

async def get_volatility_estimate(token_address: str) -> float:
    """
    Stub: renvoyer un écart-type du prix basé sur un API ou calcul local.
    Pour l'instant, on retourne une valeur fixe.
    """
    return 0.02  # 2% par défaut

async def handle_new_token(token_address: str, creation_ts: float):
    # 1️⃣ Honeypot
    if await is_honeypot(token_address):
        log.info(f"{token_address}: detected honeypot, skipping")
        return

    # 2️⃣ Récupération liquidité et score IA
    liquidity  = await get_liquidity(token_address)
    volatility = await get_volatility_estimate(token_address)
    age_secs   = time.time() - creation_ts
    tok_score  = score_token(liquidity, volatility, age_secs)
    log.info(f"{token_address}: liquidity={liquidity:.2f} SOL, volatility={volatility:.3f}, age={age_secs:.0f}s, score={tok_score:.3f}")

    if tok_score < SCORE_THRESH:
        log.info(f"{token_address}: score {tok_score:.3f} < threshold {SCORE_THRESH}, skipping")
        return

    # 3️⃣ TP/SL dynamiques
    # entrée fictive pour l’exemple
    entry_price = 1.0
    tp, sl = calculate_tp_sl(entry_price, TP_MULTIPLIER, SL_MULTIPLIER)

    # 4️⃣ Swap via Jupiter (stub)
    log.info(f"{token_address}: swapping with slippage={SLIPPAGE_BPS}bps")
    # … code swap …

    # 5️⃣ Post-snipe : envoi de l’événement au dashboard
    exit_price = entry_price * TP_MULTIPLIER  # stub
    pnl = exit_price - entry_price
    try:
        requests.post("http://localhost:8000/stats/event", json={
            "success": exit_price >= tp,
            "pnl": pnl
        })
    except Exception:
        pass

async def websocket_listener():
    import websockets
    uri = WS_URL
    async with websockets.connect(uri) as ws:
        subscribe = {
            "jsonrpc":"2.0",
            "id":1,
            "method":"getProgramAccounts",
            "params":[
                "PumpFun1zzzzzzzzzzzzzzzzzzzzzzzzzzzz",
                {"encoding":"base64","filters":[{"dataSize":165}]}
            ]
        }
        await ws.send(json.dumps(subscribe))
        async for msg in ws:
            address, ts = parse_msg(msg)
            await handle_new_token(address, ts)

async def main():
    log.info("🚀 Démarrage du bot NONO")
    await websocket_listener()

if __name__ == "__main__":
    asyncio.run(main())
