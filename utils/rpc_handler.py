# utils/rpc_handler.py
import os
import logging
from config.log_config import setup_logger

logger = setup_logger("rpc_handler")

RPC_URL_MAINNET = os.getenv("RPC_URL_MAINNET")
HELIUS_SENDER_RPC_URL = os.getenv("HELIUS_SENDER_RPC_URL")
RPC_BACKUP_URL = os.getenv("RPC_BACKUP_URL", "https://api.mainnet-beta.solana.com")

current_rpc_url = RPC_URL_MAINNET


def get_current_rpc():
    return current_rpc_url


def fallback_rpc(reason: str = "Erreur inconnue"):
    global current_rpc_url

    logger.warning(f"\U0001F6D1 Bascule RPC enclenchée: {reason}")

    if current_rpc_url == RPC_URL_MAINNET:
        current_rpc_url = HELIUS_SENDER_RPC_URL
        logger.warning("⏩ Passage au RPC Helius Sender (rapide)")
    elif current_rpc_url == HELIUS_SENDER_RPC_URL:
        current_rpc_url = RPC_BACKUP_URL
        logger.warning(f"⚡ Passage au RPC backup: {RPC_BACKUP_URL}")
    else:
        logger.error("❌ Tous les RPCs ont déjà été testés. Aucun fallback disponible.")

    # (Optionnel) notifier via webhook si URL fournie
    webhook = os.getenv("WEBHOOK_URL")
    if webhook:
        import httpx
        try:
            httpx.post(webhook, json={
                "event": "rpc_switch",
                "reason": reason,
                "new_rpc": current_rpc_url
            }, timeout=5)
        except Exception as e:
            logger.error(f"Erreur webhook fallback RPC: {e}")
