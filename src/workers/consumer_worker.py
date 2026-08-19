import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.processed_event import ProcessedEvent
from src.services.authors import AuthorService
from src.config.kafka_consumer import Consumer
from src.config.kafka_dlq_publisher import DlqPublisher
from src.db import async_session_maker
from src.utils.logger import get_logger
from src.utils.timeout import kafka_timeout
from src.config.config import settings


logger = get_logger("consumer_worker")


class ConsumerWorker:
    def __init__(
            self,
            consumer: Consumer,
            dlq: DlqPublisher,
            service: AuthorService,
            session_maker,
    ) -> None:
        self.consumer = consumer
        self.dlq = dlq
        self.service = service
        self.session_maker = session_maker

    async def start(self) -> None:
        await self.consumer.start()
        await self.dlq.start()
        logger.info("[ConsumerWorker] started")

    async def stop(self) -> None:
        await self.consumer.stop()
        await self.dlq.stop()
        logger.info("[ConsumerWorker] stopped")

    async def _is_event_processed(self, event_id: str, session: AsyncSession) -> bool:
        result = await session.execute(
            select(ProcessedEvent.event_id).where(ProcessedEvent.event_id == event_id)
        )
        return result.scalar_one_or_none() is not None

    async def _process_once(self, payload: dict) -> None:
        async with self.session_maker() as session:
            if not await self._is_event_processed(payload.get('id'), session):
                await self.service.create_author_from_message(payload, session)
                logger.info(
                    f'[ConsumerWorker] success created author'
                )
                await session.commit()

    async def _process_with_retry(self, msg) -> bool:
        """True — можно коммитить оффсет (успех или DLQ прошёл)."""
        last_error: Exception | None = None

        for attempt in range(0, settings.MAX_RETRIES):
            try:
                await self._process_once(msg.value)
                logger.info(
                    f"[ConsumerWorker] success offset={msg.offset} attempt={attempt}"
                )
                return True
            except Exception as e:
                last_error = e
                logger.warning(
                    f"[ConsumerWorker] attempt {attempt}/{settings.MAX_RETRIES} "
                    f"failed offset={msg.offset}: {e}"
                )
                if attempt + 1 != settings.MAX_RETRIES:
                    await kafka_timeout(attempt)

        logger.exception(
            f"[ConsumerWorker] retries exhausted offset={msg.offset}: {last_error}"
        )
        return await self._send_to_dlq(msg, last_error)

    async def _send_to_dlq(self, msg, error: Exception) -> bool:
        try:
            await self.dlq.send(
                original_topic=msg.topic,
                partition=msg.partition,
                offset=msg.offset,
                key=msg.key.decode("utf-8") if msg.key else None,
                payload=msg.value,
                error=str(error),
            )
            logger.info(f"[ConsumerWorker] sent to DLQ offset={msg.offset}")
            return True
        except Exception as dlq_error:
            logger.exception(
                f"[ConsumerWorker] DLQ send failed offset={msg.offset}: {dlq_error}"
            )
            return False

    async def run(self) -> None:
        await self.start()
        try:
            async for msg in self.consumer:
                logger.info(
                    f"[ConsumerWorker] received topic={msg.topic} "
                    f"partition={msg.partition} offset={msg.offset}"
                )

                can_commit = await self._process_with_retry(msg)

                if can_commit:
                    await self.consumer.commit()
                    logger.info(f"[ConsumerWorker] committed offset={msg.offset}")
                else:
                    logger.warning(
                        f"[ConsumerWorker] offset={msg.offset} not committed, "
                        f"will be redelivered"
                    )
        finally:
            await self.stop()


async def main() -> None:
    worker = ConsumerWorker(
        consumer=Consumer(),
        dlq=DlqPublisher(),
        service=AuthorService(),
        session_maker=async_session_maker,
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())