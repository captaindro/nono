from utils.creator_tracker import record_token_creation
from main import handle_new_token
import asyncio, time

async def test_live():
    mint = "4k3Dyjzvzp8eZZKCDs98U7KxYpYxYqP9JrhG4VvFSCi6"
    creator = "JBYTEiKue7TdNMWtSKUZwyyRpHpTV9UKgkioQP4JttPn"
    # Incrémente le score du créateur (si besoin) :
    record_token_creation(creator, is_rug=False)

    print("📌 Créateur enregistré :", creator)
    await handle_new_token(mint, time.time(), creator)

asyncio.run(test_live())
