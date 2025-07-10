import asyncio
from utils.logger import get_logger

logger = get_logger(__name__)

class RetryQueue:
    def __init__(self):
        self.queue = asyncio.Queue()
        self.retry_delay = 15  # secondes

    async def add(self, token_info):
        await self.queue.put(token_info)
        logger.info(f"[retry_queue] Token ajouté à la file de retry: {token_info['mint']}")

    async def process(self, handler_func):
        """
        Process la file en appelant handler_func(token_info) pour chaque élément.
        En boucle infinie avec délai.
        """
        while True:
            token_info = await self.queue.get()
            try:
                logger.info(f"[retry_queue] Retry sur token {token_info['mint']}")
                await handler_func(token_info)
            except Exception as e:
                logger.error(f"[retry_queue] Erreur lors du retry: {e}")
                # Re-ajout en queue pour tentative ultérieure
                await self.queue.put(token_info)
            await asyncio.sleep(self.retry_delay)
