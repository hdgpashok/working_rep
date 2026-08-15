import asyncio

from src.services.authors import AuthorService
from src.kafka_consumer import Consumer
from src.kafka_dlq_publisher import DlqPublisher
from src.db import async_session_maker
from src.utils.logger import get_logger

logger = get_logger("consumer_worker")


class ConsumerWorker:
    def __init__(self) -> None:
        self.consumer = Consumer()
        self.dlq = DlqPublisher()
        self.service = AuthorService()

    async def start(self) -> None:
        await self.consumer.start()
        await self.dlq.start()
        logger.info("[ConsumerWorker] started")

    async def stop(self) -> None:
        await self.consumer.stop()
        await self.dlq.stop()
        logger.info("[ConsumerWorker] stopped")

    async def process_message(self, payload: dict) -> None:
        async with async_session_maker() as session:
            await self.service.create_author_from_message(payload, session)
            await session.commit()

    async def run(self) -> None:
        await self.start()

        try:
            async for msg in self.consumer:
                logger.info(
                    f"[ConsumerWorker] received topic={msg.topic} "
                    f"partition={msg.partition} offset={msg.offset}"
                )

                try:
                    await self.process_message(msg.value)
                    await self.consumer.commit()
                    logger.info(f"[ConsumerWorker] success offset={msg.offset}")

                except Exception as e:
                    logger.exception(
                        f"[ConsumerWorker] processing failed offset={msg.offset}: {e}"
                    )

                    try:
                        await self.dlq.send(
                            original_topic=msg.topic,
                            partition=msg.partition,
                            offset=msg.offset,
                            key=msg.key.decode("utf-8") if msg.key else None,
                            payload=msg.value,
                            error=str(e),
                        )
                        logger.info(f"[ConsumerWorker] sent to DLQ offset={msg.offset}")
                    except Exception as dlq_error:
                        logger.exception(
                            f"[ConsumerWorker] DLQ send failed offset={msg.offset}: {dlq_error}"
                        )

                    await self.consumer.commit()
                    logger.info(f"[ConsumerWorker] committed after error offset={msg.offset}")

        finally:
            await self.stop()


async def main() -> None:
    worker = ConsumerWorker()
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())