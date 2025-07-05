#!/usr/bin/env python3
import os
import time
import json
import asyncio
import logging
import requests
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

from utils.honeypot import is_honeypot
from utils.liquidity import get_liquidity
from utils.tp_sl import calculate_tp_sl
from utils.scoring import score_token
from utils.jupiter import execute_swap

from solana.keypair import Keypair

# Paramètres dynamiques
TP_MULTIPLIER = float(os.getenv("take_profit_multiplier", 1.1))
SL_MULTIPLIER = float(os.getenv("stop_loss_multiplier", 0.8))
SLIPPAGE_BPS  = int(os.getenv("slippage_bps", 50))
LIQ_THRESH    = float(os.getenv("liquidity_threshold_sol", 0.5))
SCORE_THRESH  = float(os.getenv("token_score_threshold", 0.7))

# Environnement
ENV    = os.getenv("ENVIRONMENT", "mainnet").lower()
WS_URL = os.getenv("WS_URL_MAINNET") if ENV == "mainnet" else os.getenv("WS_URL_DEVNET")
WALLET_PATH = os.getenv("WALLET_PATH")

# Programme Pump.fun
PUMP_FUN_PROGRAM_ID = "PumpFun1zzzzzzzzzzzzzzzzzzzzzzzzzzzz"

# Logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s"
)
log = logging.getLogger("nono")

async def get_volatility_estimate(_):
    return 0.02  # stub

async def handle_new_token(token_address: str, creation_ts: float):
    log.info(f"👉 Nouveau token détecté : {token_address}")

    if await is_honeypot(token_address):
        log.info(f"{token_address}: honeypot détecté, skip")
        return

    liquidity  = await get_liquidity(token_address)
    volatility = await get_volatility_estimate(token_address)
    age_secs   = time.time() - creation_ts
    tok_score  = score_token(liquidity, volatility, age_secs)
    log.info(f"{token_address}: liq={liquidity:.2f} SOL, vol={volatility:.3f}, age={age_secs:.0f}s, score={tok_score:.3f}")

    if tok_score < SCORE_THRESH:
        log.info(f"{token_address}: score {tok_score:.3f} < seuil {SCORE_THRESH}, skip")
        return

    # Calcul TP/SL
    entry_price = 1.0  # placeholder
    tp, sl = calculate_tp_sl(entry_price, TP_MULTIPLIER, SL_MULTIPLIER)
    log.info(f"{token_address}: TP={tp:.3f}, SL={sl:.3f}")

    # Exécution du swap via Jupiter
    # Charge le signer depuis WALLET_PATH
    kp_bytes = json.loads(Path(WALLET_PATH).read_text())
    signer = Keypair.from_secret_key(bytes(kp_bytes))
    ok = await execute_swap(
        wallet_pubkey=signer.public_key.to_base58().decode(),
        wallet_signer=signer,
        input_mint="So11111111111111111111111111111111111111112",
        output_mint=token_address,
        amount=int(1e9),
        slippage_bps=SLIPPAGE_BPS
    )
    if not ok:
        log.error(f"{token_address}: swap échoué")
        return

    # Envoi d'un event au dashboard
    exit_price = entry_price * TP_MULTIPLIER  # placeholder
    pnl = exit_price - entry_price
    try:
        requests.post(
            "http://localhost:3000/stats/event",
            json={"success": exit_price >= tp, "pnl": pnl},
            timeout=2
        )
    except Exception as e:
        log.warning(f"Erreur envoi stats: {e}")

async def websocket_listener():
    import websockets

    if not WS_URL or not WS_URL.startswith(("ws://", "wss://")):
        log.error(f"WS_URL invalide : {WS_URL!r}")
        return

    log.info(f"🔌 Connexion WS → {WS_URL}")
    async with websockets.connect(WS_URL) as ws:
        log.info("✅ WS connecté")

        # programSubscribe Pump.fun
        msg = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "programSubscribe",
            "params": [
                PUMP_FUN_PROGRAM_ID,
                {"encoding": "jsonParsed", "filters": [{"dataSize": 165}]}
            ]
        }
        await ws.send(json.dumps(msg))
        log.debug(f"> TEXT {json.dumps(msg)}")

        async for raw in ws:
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                log.debug(f"Invalid JSON raw: {raw}")
                continue

            notif = data.get("params", {}).get("result", {})
            value = notif.get("value")
            if not value:
                log.debug(f"WS non-notif: {raw}")
                continue

            parsed = value.get("account", {}).get("data", {}).get("parsed", {})
            info   = parsed.get("info", {})
            token_address = info.get("mint")
            if not token_address:
                log.debug(f"Notif sans mint: {raw}")
                continue

            await handle_new_token(token_address, time.time())

async def main():
    log.info("🚀 Démarrage du bot NONO")
    await websocket_listener()

if __name__ == "__main__":
    asyncio.run(main())
