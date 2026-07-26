import asyncio
import json

from aiokafka import AIOKafkaConsumer

from src.utils.config import settings


def deserializer(message):
    return json.loads(message)


async def event_handler(value):
    print(f"temperature {value['temp']}, weather {value['weather']}")


async def consume():
    consumer = AIOKafkaConsumer(
        settings.KAFKA_TOPIC,
        bootstrap_servers=f'{settings.KAFKA_HOST}:{settings.KAFKA_PORT}',
        value_deserializer=deserializer,

    )
    await consumer.start()

    try:
        async for msg in consumer:
            await event_handler(msg.value)
    finally:
        await consumer.stop()


if __name__ == '__main__':
    asyncio.run(consume())