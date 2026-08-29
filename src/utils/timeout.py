
import random

import asyncio

from src.config.config import settings


async def timeout_with_jitter(attempt: int):
    delay = 0.1 * (2 ** attempt)
    jitter = random.uniform(0, delay * 0.3)
    await asyncio.sleep(delay + jitter)


async def kafka_timeout(attempt: int):
    delay = settings.BASE_KAFKA_DELAY * (2 ** attempt)
    jitter = jitter = random.uniform(0, delay * 0.3)
    await asyncio.sleep(delay + jitter)