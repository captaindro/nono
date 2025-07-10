import httpx

async def test_jupiter_quote(mint_address):
    url = "https://quote-api.jup.ag/v6/quote"
    params = {
        "inputMint": "So11111111111111111111111111111111111111112",  # SOL
        "outputMint": mint_address,
        "amount": int(0.005 * 10**9),  # 0.005 SOL en lamports
        "slippageBps": 500
    }

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
        print(resp.status_code)
        print(resp.text)

import asyncio
if __name__ == "__main__":
    asyncio.run(test_jupiter_quote("6G4PHTnkLu7rT9eEvAZE7kUgEVtEqFRs9nEbJrc1rFAU"))
