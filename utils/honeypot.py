import logging
import httpx

log = logging.getLogger("utils.honeypot")

async def is_honeypot(mint: str, amount: float) -> bool:
    url = f"https://quote-api.jup.ag/v4/swap/simulate?mintIn={mint}&mintOut=So11111111111111111111111111111111111111112&amount=10000000&slippageBps=50&userPublicKey=4ACfpUFoaSD9bfPdeu6DBt89gB6ENTeHBXCAi87NhDEE"
    log.debug(f"🔍 Simulate honeypot: {url}")
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url)
        if resp.status_code == 404:
            log.warning(f"{mint}: 🚫 Token non trouvé dans Jupiter (404)")
            return True
        return False
    except Exception as e:
        log.error(f"{mint}: erreur simulation Jupiter: {e}")
        return True