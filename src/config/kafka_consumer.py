import json

from aiokafka import AIOKafkaConsumer

from config.config import settings


def deserializer(message):
    return json.loads(message)


class Consumer:
    def __init__(self):
        self.consumer = AIOKafkaConsumer

    async def start(self):
        self.consumer = AIOKafkaConsumer(
            settings.KAFKA_TOPIC,
            bootstrap_servers=f'{settings.KAFKA_HOST}:{settings.KAFKA_PORT}',
            value_deserializer=deserializer,
            group_id=settings.KAFKA_GROUP_ID,
            enable_auto_commit=False,
            auto_offset_reset='earliest',
        )
        await self.consumer.start()

    async def stop(self):
        if self.consumer:
            await self.consumer.stop()
        return

    async def commit(self):
        if self.consumer:
            await self.consumer.commit()
        return

    def __aiter__(self):
        if self.consumer is None:
            raise RuntimeError("Consumer is not started")
        return self.consumer.__aiter__()