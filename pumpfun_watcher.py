# pumpfun_watcher.py

import asyncio
import httpx
import logging
from utils.config import load_config

log = logging.getLogger("watcher")
seen_mints = set()

async def watch_pumpfun(token_queue):
    url = "https://pump.fun/board?coins_sort=created_timestamp"

    while True:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.get(url)
                if resp.status_code != 200:
                    log.warning(f"⚠️ Erreur HTTP {resp.status_code} depuis Pump.fun")
                    await asyncio.sleep(3)
                    continue

                content = resp.text
                new_mints = extract_mints_from_html(content)
                for mint in new_mints:
                    if mint not in seen_mints:
                        seen_mints.add(mint)
                        log.info(f"🧩 Nouveau mint détecté via scraping: {mint}")
                        await token_queue.put({"creator": None, "mint": mint})
        except Exception as e:
            log.error(f"❌ Erreur lors du scraping Pump.fun : {e}")

        await asyncio.sleep(3)

def extract_mints_from_html(html):
    import re
    matches = re.findall(r"https://pump\.fun/coin/([A-Za-z0-9]{32,44})", html)
    return matches
