import asyncio
import json
import os

from aiokafka import AIOKafkaConsumer

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
TOPIC_NAME = os.getenv("TOPIC_NAME", "demo-topic")
GROUP_ID = os.getenv("GROUP_ID", "demo-group")


async def consume() -> None:
    consumer = AIOKafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=GROUP_ID,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        auto_offset_reset="earliest",
    )

    await consumer.start()
    print(f"Consumer listening on topic '{TOPIC_NAME}' …")
    try:
        async for msg in consumer:
            print(
                f"Consumed → partition={msg.partition} offset={msg.offset} value={msg.value}"
            )
    finally:
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(consume()) 