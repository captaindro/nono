# scraper.py

import asyncio
import logging
import httpx
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Set

from config.settings import settings
# from utils.filters.token_passes_filters import token_passes_filters

logger = logging.getLogger("scraper")

PUMP_FUN_HTML_URL = "https://pump.fun/board?coins_sort=created_timestamp"
SCRAPER_INTERVAL_SECONDS = settings.scraper_interval_seconds

_seen_tokens: Set[str] = set()


async def fetch_pumpfun_html() -> str:
    """Télécharge la page Pump.fun en HTML."""
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(PUMP_FUN_HTML_URL)
        r.raise_for_status()
        return r.text


def parse_tokens_from_html(html: str) -> list[dict]:
    """Extrait les tokens du HTML."""
    soup = BeautifulSoup(html, "html.parser")
    tokens = []
    cards = soup.select("div.board-card")
    for card in cards:
        try:
            name = card.select_one("div.text-white").get_text(strip=True)
            symbol = None
            for d in card.find_all("div"):
                t = d.get_text(strip=True)
                if t.startswith("(") and t.endswith(")"):
                    symbol = t
                    break
            creator = "unknown"
            parent = card.parent
            if parent:
                for sib in parent.find_all_next("div", limit=3):
                    tx = sib.get_text(strip=True).lower()
                    if "created by" in tx:
                        creator = sib.get_text(strip=True).replace("created by", "").strip()
                        break
            token_address = None
            if parent:
                for a in parent.find_all("a", href=True):
                    if "/token/" in a["href"]:
                        token_address = a["href"].split("/token/")[-1]
                        break
            if token_address and name:
                tokens.append({"address": token_address, "name": name, "symbol": symbol, "creator": creator})
        except Exception:
            continue
    return tokens


async def start_scraper(callback):
    """
    Scraper Pump.fun :
    - récupère le HTML
    - parse les tokens
    - détecte les nouveaux (via _seen_tokens)
    - appelle callback(address, creator) pour chacun
    """
    global _seen_tokens

    while True:
        try:
            html = await fetch_pumpfun_html()
            # Pour debug, décommentez pour enregistrer snapshot :
            # open("debug_pumpfun.html","w",encoding="utf-8").write(html)

            tokens = parse_tokens_from_html(html)
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new = [t for t in tokens if t["address"] not in _seen_tokens]
            _seen_tokens.update(t["address"] for t in new)
            logger.info(f"[SCRAPER] {now} - {len(new)} nouveaux tokens détectés")
            for t in new:
                await callback(t["address"], t["creator"])
        except Exception as e:
            logger.error(f"❌ Erreur scraper : {e}", exc_info=True)

        await asyncio.sleep(SCRAPER_INTERVAL_SECONDS)
