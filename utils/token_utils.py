import aiohttp
import json
from loguru import logger as log
from config.settings import settings

# ⚠️ Liste des mints déjà vus durant la session (évite les doublons)
seen_tokens = set()


def is_token_already_seen(mint: str) -> bool:
    """Retourne True si le token a déjà été traité"""
    return mint in seen_tokens


def mark_token_as_seen(mint: str) -> None:
    """Ajoute un token à la liste des tokens vus"""
    seen_tokens.add(mint)


async def get_token_liquidity(token_address: str):
    """
    Récupère la liquidité actuelle du token (en SOL) via Jupiter quote API.
    Retourne (inputMint, outputMint, outAmount) si une route est trouvée.
    """
    url = f"{settings.jupiter_api_url}/v6/quote"
    params = {
        "inputMint": "So11111111111111111111111111111111111111112",  # SOL
        "outputMint": token_address,
        "amount": int(settings.quote_amount),
        "slippageBps": settings.slippage_bps,
        "onlyDirectRoutes": str(settings.jupiter_only_direct_routes).lower()
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=8) as resp:
                if resp.status != 200:
                    log.warning(f"[JUPITER] ❌ Erreur HTTP {resp.status} pour {token_address}")
                    return None

                data = await resp.json()

                if settings.EXPERT_MODE:
                    log.debug(f"[JUPITER] Réponse brute pour {token_address}:\n{json.dumps(data, indent=2)}")

                if "outAmount" in data and "routePlan" in data:
                    input_mint = data["inputMint"]
                    output_mint = data["outputMint"]
                    out_amount = float(data["outAmount"]) / 1e9
                    return input_mint, output_mint, out_amount

                log.warning(f"[JUPITER] ❌ Aucune route disponible pour {token_address}")
                return None

    except Exception as e:
        log.exception(f"[JUPITER] ⚠️ Erreur get_token_liquidity pour {token_address}: {e}")
        return None


async def get_token_name(token_address: str) -> str:
    """
    Récupère le nom du token via l'API publique Birdeye.
    """
    try:
        url = f"https://public-api.birdeye.so/public/token/{token_address}"
        headers = {"x-chain": "solana"}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=8) as resp:
                if resp.status != 200:
                    log.warning(f"[BIRDEYE] ❌ Erreur HTTP {resp.status} pour {token_address}")
                    return token_address[:6] + "..."

                data = await resp.json()
                name = data.get("data", {}).get("name", "")
                return name if name else token_address[:6] + "..."

    except Exception as e:
        log.warning(f"[BIRDEYE] ⚠️ Erreur récupération nom pour {token_address}: {e}")
        return token_address[:6] + "..."
