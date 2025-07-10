import logging
from solders.keypair import Keypair
from solana.rpc.async_api import AsyncClient
import json
import asyncio

logger = logging.getLogger("nono")

class JupiterSwap:
    def __init__(self, amount_in_sol=0.005):
        self.amount_in_sol = amount_in_sol
        self.wallet_path = "wallets/wallet.json"
        self.client = AsyncClient("https://api.mainnet-beta.solana.com")
        self.keypair = self.load_keypair()
        self.jupiter = JupiterAggregator(self.client, self.keypair)

        with open(self.wallet_path, "r") as f:
            secret_key = json.load(f)
            return Keypair.from_bytes(bytes(secret_key))

    async def swap_sol_to_token(self, mint_token: str):
        try:
            routes = await self.jupiter.get_routes("So11111111111111111111111111111111111111112", mint_token, int(self.amount_in_sol * 1e9))
            if not routes:
                logger.warning(f"❌ Aucun swap possible pour {mint_token}")
                return False
            route = routes[0]
            tx = await self.jupiter.exchange(route)
            logger.debug(f"🔄 TX achat envoyé : {tx}")
            return True
        except Exception as e:
            logger.error(f"Erreur lors du swap vers {mint_token} : {e}")
            return False

    async def swap_token_to_sol(self, mint_token: str):
        try:
            routes = await self.jupiter.get_routes(mint_token, "So11111111111111111111111111111111111111112", int(self.amount_in_sol * 1e9 * 0.95))
            if not routes:
                logger.warning(f"❌ Aucun swap retour possible pour {mint_token}")
                return False
            route = routes[0]
            tx = await self.jupiter.exchange(route)
            logger.debug(f"🔄 TX vente envoyée : {tx}")
            return True
        except Exception as e:
            logger.error(f"Erreur lors du swap retour depuis {mint_token} : {e}")
            return False
