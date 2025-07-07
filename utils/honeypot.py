import httpx
import logging
import os

log = logging.getLogger("honeypot")

JUPITER_SIM_URL = "https://quote-api.jup.ag/v4/swap/simulate"

async def is_honeypot(token_mint: str, amount: int) -> bool:
    """
    Vérifie si un token est un honeypot en utilisant l'API de simulation de Jupiter.
    Retourne True si le swap échoue (donc possiblement un honeypot), False sinon.
    """
    try:
        url = (
            f"{JUPITER_SIM_URL}"
            f"?mintIn={token_mint}"
            f"&mintOut=So11111111111111111111111111111111111111112"
            f"&amount={amount}"
            f"&slippageBps={os.getenv('slippage_bps', 50)}"
            f"&userPublicKey={os.getenv('WALLET_PUBLIC_KEY')}"
        )

        log.debug(f"🔍 Simulate honeypot: {url}")

        async with httpx.AsyncClient(timeout=3) as client:
            response = await client.get(url)

        # Considérer comme honeypot si erreur HTTP
        if response.status_code != 200:
            log.error(f"{token_mint}: ❌ Simulate status={response.status_code}")
            return True

        return False

    except Exception as e:
        log.error(f"{token_mint}: ❌ Exception pendant is_honeypot: {e}")
        return True
