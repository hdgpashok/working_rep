import asyncio

from sqlalchemy.exc import IntegrityError, DataError, OperationalError
from sqlalchemy.exc import TimeoutError as SATimeoutError
from aiokafka.errors import KafkaConnectionError, KafkaTimeoutError, RequestTimedOutError

from aiokafka import AIOKafkaConsumer, TopicPartition

from config.config import settings


TRANSIENT_ERRORS = (
    OperationalError,
    SATimeoutError,
    asyncio.TimeoutError,
    KafkaConnectionError,
    KafkaTimeoutError,
    RequestTimedOutError,
)

NON_RETRYABLE_ERRORS = (
    ValueError,
    KeyError,
    IntegrityError,
    DataError,
)


class Consumer:
    def __init__(self):
        self.consumer = None
        self._lock = asyncio.Lock()

    async def start(self) -> None:
        async with self._lock:
            if self.consumer is None:
                self.consumer = AIOKafkaConsumer(
                    settings.KAFKA_TOPIC,
                    bootstrap_servers=f'{settings.KAFKA_HOST}:{settings.KAFKA_PORT}',
                    group_id=settings.KAFKA_GROUP_ID,
                    enable_auto_commit=False,
                    auto_offset_reset='earliest',
                )
                await self.consumer.start()
            return

    async def stop(self) -> None:
        async with self._lock:
            if self.consumer:
                await self.consumer.stop()
                self.consumer = None
            return

    async def commit(self) -> None:
        if self.consumer:
            await self.consumer.commit()
        return

    async def commit_offset(self, topic: str, partition: int, offset: int) -> None:
        if self.consumer:
            tp = TopicPartition(topic, partition)
            await self.consumer.commit({tp: offset + 1})
        return

    def __aiter__(self) -> AIOKafkaConsumer:
        if self.consumer is None:
            raise RuntimeError("Consumer is not started")
        return self.consumer.__aiter__()