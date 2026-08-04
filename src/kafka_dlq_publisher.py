from datetime import datetime, timezone
import json

from aiokafka import AIOKafkaProducer

from src.utils.config import settings
from src.utils.logger import get_logger

logger = get_logger("dlq_publisher")


def serializer(message: dict) -> bytes:
    return json.dumps(message).encode("utf-8")


class DlqPublisher:
    def __init__(self) -> None:
        self.producer: AIOKafkaProducer | None = None

    async def start(self) -> None:
        self.producer = AIOKafkaProducer(
            bootstrap_servers=f"{settings.KAFKA_HOST}:{settings.KAFKA_PORT}",
            value_serializer=serializer,
            enable_idempotence=True,
            acks="all",
        )
        await self.producer.start()
        logger.info("[DLQ] Publisher started")

    async def stop(self) -> None:
        if self.producer is None:
            return
        try:
            await self.producer.stop()
            logger.info("[DLQ] Publisher stopped")
        finally:
            self.producer = None

    async def send(
            self,
            *,
            original_topic: str,
            partition: int,
            offset: int,
            key: str | None,
            payload: dict,
            error: str,
    ) -> None:
        if self.producer is None:
            raise RuntimeError("DlqPublisher is not started")

        message = {
            "original_topic": original_topic,
            "partition": partition,
            "offset": offset,
            "key": key,
            "payload": payload,
            "error": error,
            "failed_at": datetime.now(timezone.utc).isoformat(),
        }

        await self.producer.send_and_wait(
            topic=settings.KAFKA_DLQ_TOPIC,
            value=message,
            key=key.encode("utf-8") if key else None,
        )
        logger.info(
            f"[DLQ] Sent to DLQ topic={settings.KAFKA_DLQ_TOPIC} "
            f"offset={offset} partition={partition} error={error}"
        )