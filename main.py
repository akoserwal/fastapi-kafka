import json
import os
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel
from aiokafka import AIOKafkaProducer
import asyncio
from contextlib import asynccontextmanager


# --- Lifespan context -------------------------------------------------------


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage Kafka producer lifecycle using FastAPI lifespan."""
    global producer
    # Startup: connect with retries
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            producer = AIOKafkaProducer(
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            )
            await producer.start()
            print("Kafka producer connected ✔️")
            break
        except Exception as exc:
            print(
                f"Kafka connection attempt {attempt}/{MAX_RETRIES} failed: {exc}"
            )
            if attempt == MAX_RETRIES:
                raise
            await asyncio.sleep(RETRY_DELAY_SEC)

    yield  # --- App is running ---

    # Shutdown: close producer
    if producer is not None:
        await producer.stop()
        print("Kafka producer stopped.")


# FastAPI application
app = FastAPI(title="Kafka Event-Driven Demo with FastAPI", lifespan=lifespan)

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
TOPIC_NAME = os.getenv("TOPIC_NAME", "demo-topic")

producer: AIOKafkaProducer | None = None

# Retry settings for connecting to Kafka. Change via env vars if needed.
MAX_RETRIES = int(os.getenv("KAFKA_CONNECT_RETRIES", "10"))
RETRY_DELAY_SEC = float(os.getenv("KAFKA_CONNECT_RETRY_DELAY", "2"))


class Message(BaseModel):
    """Schema for incoming POST payloads."""

    message: Any


@app.post("/publish")
async def publish_message(msg: Message):
    """Publish a JSON message to the configured Kafka topic."""
    if producer is None:
        return {"error": "Producer not ready"}

    await producer.send_and_wait(TOPIC_NAME, msg.dict())
    return {"topic": TOPIC_NAME, "status": "sent"} 