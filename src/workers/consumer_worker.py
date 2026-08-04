import asyncio

from src.services.users import UserService
from src.kafka_consumer import Consumer

from src.db import async_session_maker


class ConsumerWorker:
    def __init__(self):
        self.consumer = Consumer()
        self.service = UserService()

    async def start(self):
        await self.consumer.start()

    async def stop(self):
        await self.consumer.stop()

    async def process_batch(self, payload: dict):
        async with async_session_maker() as session:
            await self.service.create_user_from_message(payload, session)
            await session.commit()

    async def run(self):
        await self.start()

        try:
            async for msg in self.consumer:
                try:
                    await self.process_batch(msg.value)
                    await self.consumer.commit()
                except Exception as e:
                    # dlq
                    await self.consumer.commit()
        finally:
            await self.stop()


async def main():
    worker = ConsumerWorker()
    await worker.run()


if __name__ == '__main__':
    asyncio.run(main())