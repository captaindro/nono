import asyncio
import time
import os
from dotenv import load_dotenv
from solders.pubkey import Pubkey

from utils.jup_swap import execute_swap
from utils.filters import is_honeypot, has_enough_liquidity, get_token_score

load_dotenv()

# Mints
SOL_MINT = "So11111111111111111111111111111111111111112"
BASE_AMOUNT_SOL = 0.005  # À adapter selon ta stratégie

async def buy_token_with_jupiter(token_mint: str, amount_sol: float = BASE_AMOUNT_SOL):
    print(f"🟢 Tentative d'achat du token {token_mint} pour {amount_sol} SOL...")

    try:
        swap = JupiterSwap()
        amount_lamports = int(amount_sol * 1_000_000_000)

        tx = await swap.swap(
            input_mint=SOL_MINT,
            output_mint=token_mint,
            amount=amount_lamports,
            slippage_bps=int(os.getenv("slippage_bps", 50))
        )
        print("✅ Swap effectué ! TX:", tx)
        return tx

    except Exception as e:
        print("❌ Erreur lors du swap:", e)
        return None

async def sell_token_after_delay(token_mint: str, delay: int = 3):
    print(f"⏳ Attente de {delay} secondes avant la revente...")
    await asyncio.sleep(delay)

    try:
        swap = JupiterSwap()

        # 💡 Pour vendre, on suppose que l’on veut swap le token en SOL
        # ⚠️ Il faudrait d'abord connaître le solde du token_mint détenu.
        amount_to_sell = 1  # ← à remplacer dynamiquement plus tard
        tx = await swap.swap(
            input_mint=token_mint,
            output_mint=SOL_MINT,
            amount=amount_to_sell,
            slippage_bps=int(os.getenv("slippage_bps", 50))
        )
        print("💰 Revente effectuée ! TX:", tx)
        return tx
    except Exception as e:
        print("❌ Erreur lors de la revente:", e)
        return None

async def evaluate_and_buy(token_mint: str):
    print(f"🔎 Analyse du token: {token_mint}")

    if await is_honeypot(token_mint):
        print("🚨 Honeypot détecté, on skip.")
        return

    if not await has_enough_liquidity(token_mint):
        print("💧 Liquidité insuffisante, on skip.")
        return

    score = await get_token_score(token_mint)
    print(f"📊 Score AI du token: {score:.2f}")

    threshold = float(os.getenv("token_score_threshold", 0.7))
    if score < threshold:
        print(f"📉 Score trop faible ({score:.2f} < {threshold}), skip.")
        return

    # ✅ Tous les critères sont remplis, on achète
    tx = await buy_token_with_jupiter(token_mint)

    # Revente automatique après délai
    if tx:
        await sell_token_after_delay(token_mint, delay=3)
