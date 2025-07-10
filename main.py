<<<<<<< HEAD
import asyncio
import json
import logging
import time

from utils.parser import parse_msg
from utils.honeypot import is_honeypot
from utils.liquidity import get_liquidity
from utils.jup_swap import buy_token, sell_token
from utils.scoring import score_token
from utils.creator_tracker import record_token_creation, is_suspicious

import websockets

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("main")

RPC_WSS_URL = "wss://mainnet.helius-rpc.com/?api-key=75c7c75c-0230-482e-af0e-f2860324e474"
PUMP_PROGRAM = "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"

# Verrou global pour empêcher plusieurs achats
already_bought = asyncio.Event()

async def handle_new_token(mint: str, timestamp: float, creator_wallet: str):
    if already_bought.is_set():
        return

    log.info(f"👉 Nouveau token détecté : {mint}")

    # Enregistre le créateur
    record_token_creation(creator_wallet, is_rug=False)
    log.info(f"📌 Créateur enregistré : {creator_wallet}")

    # Ignore les créateurs suspects (beaucoup de rugs)
    if is_suspicious(creator_wallet):
        log.warning(f"⛔ Créateur suspect {creator_wallet}, token ignoré")
        return

    # Vérifie honeypot
    try:
        is_hp = await is_honeypot(mint, amount=0.01)
        if is_hp:
            log.info(f"{mint}: honeypot détecté, skip")
            return
    except Exception as e:
        log.warning(f"{mint}: erreur honeypot check: {e}")
        return

    # Vérifie liquidité
    try:
        liquidity_ok = await get_liquidity(mint)
        if not liquidity_ok:
            log.info(f"{mint}: pas assez de liquidité, skip")
            return
    except Exception as e:
        log.warning(f"{mint}: erreur get_liquidity: {e}")
        return

    # Scoring
    score = await score_token(mint)
    if score < 0.5:
        log.info(f"{mint}: score trop bas ({score:.2f}), skip")
        return

    # Achat
    try:
        amount = 0.01
        buy_resp = await buy_token(mint, amount)
        if not buy_resp:
            log.error(f"{mint}: échec achat")
            return
        already_bought.set()  # Marque qu'on a acheté
        log.info(f"✅ Achat réussi {mint}")
    except Exception as e:
        log.error(f"{mint}: erreur achat: {e}")
        return

    # Attente 3s puis revente automatique
    try:
        await asyncio.sleep(3)
        log.info(f"⏱ Revente automatique de {mint} après 3s")
        await sell_token(mint, amount)
    except Exception as e:
        log.warning(f"{mint}: erreur revente auto: {e}")

async def main():
    log.info("🚀 Démarrage du bot NONO")
    async with websockets.connect(RPC_WSS_URL) as ws:
        log.info("✅ WS connecté")
        sub_msg = json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "programSubscribe",
            "params": [
                PUMP_PROGRAM,
                {"encoding": "jsonParsed", "filters": [{"dataSize": 165}]}
            ]
        })
        await ws.send(sub_msg)

        while True:
            raw_msg = await ws.recv()
            try:
                mint, timestamp = parse_msg(raw_msg)
                creator_wallet = mint[:44]  # temporaire (TODO: extraire réellement)
                asyncio.create_task(handle_new_token(mint, timestamp, creator_wallet))
            except Exception:
                log.debug(f"WS non-notif: {raw_msg}")
                continue

if __name__ == "__main__":
    asyncio.run(main())
=======
# main.py

import asyncio
from dotenv import load_dotenv

# Charger .env **avant** tout import de config/settings
load_dotenv()

import os
from config.settings import settings
from config.log_config import setup_logger
from utils.notifier import send_email_notification
from helius_mint_listener import listen_for_mint_tokens
from scraper import start_scraper

logger = setup_logger()


async def handle_token_event(token_address: str, creator_address: str = None):
    try:
        logger.info(f"📦 Nouveau token détecté : {token_address}")

        # Traiter l’achat + revente
        from core.trading import try_buy_and_sell  # importer ici pour éviter circular import
        from utils.token_utils import get_token_name

        token_name = await get_token_name(token_address)
        wallet_used, success = await try_buy_and_sell(token_address)

        if success:
            logger.success(f"✅ Achat/Revente réussi pour {token_name} ({token_address})")
            if not settings.simulate_only:
                send_email_notification(
                    subject="✅ Achat/Revente effectuée",
                    message=f"Le bot a acheté et revendu {token_name} ({token_address}) avec le wallet {wallet_used}."
                )
        else:
            logger.warning(f"❌ Échec pour {token_name} ({token_address})")
            send_email_notification(
                subject="❌ Échec swap/revente",
                message=f"Le bot a échoué sur le token {token_name} ({token_address}) avec le wallet {wallet_used}."
            )

    except Exception as e:
        logger.error(f"❌ Erreur critique sur {token_address}", exc_info=True)
        send_email_notification(
            subject="⚠️ Erreur critique",
            message=f"Erreur pendant le traitement du token {token_address} :\n\n{e}"
        )


async def main():
    logger.info("🚀 Lancement du bot NONO...")

    tasks = []
    if settings.scraper_enabled:
        tasks.append(asyncio.create_task(start_scraper(handle_token_event)))
    tasks.append(asyncio.create_task(listen_for_mint_tokens(handle_token_event)))

    try:
        # Boucle principale
        while True:
            await asyncio.sleep(60)
    except KeyboardInterrupt:
        logger.info("🛑 Arrêt demandé, annulation des tâches…")
        for t in tasks:
            t.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        logger.info("✅ Bot arrêté proprement.")


if __name__ == "__main__":
    asyncio.run(main())
>>>>>>> 2553739 (Ajout de la config Railway et du workflow CI/CD)
