import asyncio
from utils.jupiter_swap import JupiterSwap

async def main():
    jupiter = JupiterSwap()
    sig = await jupiter.swap(
        input_mint="So11111111111111111111111111111111111111112",  # Wrapped SOL
        output_mint="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",  # USDC
        amount=10000000  # 0.01 SOL
    )
    print(f"✅ Swap envoyé ! Signature : {sig}")
    await jupiter.close()

if __name__ == "__main__":
    asyncio.run(main())
