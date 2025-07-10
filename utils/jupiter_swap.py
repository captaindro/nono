import aiohttp
import asyncio
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solana.rpc.async_api import AsyncClient
from solders.transaction import VersionedTransaction

from wallets.wallet import load_keypair_from_json


class JupiterSwap:
    def __init__(self):
        self.wallet = load_keypair_from_json()
        self.public_key = str(self.wallet.pubkey())
        self.client = AsyncClient("https://api.mainnet-beta.solana.com")
        self.session = aiohttp.ClientSession()

    async def get_quote(self, input_mint, output_mint, amount):
        url = (
            "https://quote-api.jup.ag/v6/quote"
            f"?inputMint={input_mint}"
            f"&outputMint={output_mint}"
            f"&amount={amount}"
            f"&slippageBps=100"
            f"&swapMode=ExactIn"
            f"&onlyDirectRoutes=false"
        )
        async with self.session.get(url) as resp:
            if resp.status != 200:
                raise Exception(f"Erreur quote: {resp.status}")
            data = await resp.json()
            return data["swapTransaction"], data["routePlan"][0]["amountOut"]

    async def swap(self, input_mint, output_mint, amount):
        print("🔁 Simulation quote Jupiter...")
        try:
            transaction_b64, amount_out = await self.get_quote(input_mint, output_mint, amount)
            print("✅ Quote reçu.")
        except Exception as e:
            print("⚠️ Échec de la quote:", e)
            return None

        print("🚀 Demande de transaction Jupiter...")
        url = "https://quote-api.jup.ag/v6/swap"
        payload = {
            "userPublicKey": self.public_key,
            "wrapUnwrapSOL": True,
            "feeAccount": None,
            "quoteResponse": {
                "routePlan": [],
                "amountOut": amount_out,
            },
        }

        # Simulation avec transaction récupérée précédemment
        try:
            tx_bytes = await self._decode_and_sign_transaction(transaction_b64)
            print("📦 Transaction signée, envoi en cours...")
            sig = await self.client.send_raw_transaction(tx_bytes)
            await self.client.confirm_transaction(sig.value)
            print("✅ Transaction confirmée !")
            return sig.value
        except Exception as e:
            print("❌ Envoi échoué :", e)
            return None

    async def _decode_and_sign_transaction(self, tx_b64):
        import base64
        tx_bytes = base64.b64decode(tx_b64)
        versioned_tx = VersionedTransaction.from_bytes(tx_bytes)
        versioned_tx.sign([self.wallet])
        return versioned_tx.serialize()

    async def close(self):
        await self.session.close()
