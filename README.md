# Event-Driven Architecture with FastAPI & Kafka 🚀

This example demonstrates **Kafka basics** using **Python FastAPI** as a _producer_ and an asynchronous standalone script as a _consumer_. It is meant to be a gentle introduction to event-driven systems.

---

## Why Event-Driven?

1. **Loose coupling** – services exchange events rather than call each other directly.
2. **Scalability** – producers and consumers scale independently.
3. **Resilience** – if a consumer is down, messages are persisted in Kafka until it comes back.
4. **Extensibility** – new consumers can be added without touching existing producers.

## Kafka Primer

* **Topic** – named stream of records (our example uses `demo-topic`).
* **Producer** – application that sends records (FastAPI endpoint).
* **Consumer** – application that reads records (`consumer.py`).
* **Broker** – Kafka server that stores topics.

![Event Flow](https://mermaid.ink/img/pako:eNptj11vgzAUxu_8Ct27RFbpNt2EqkE7UpglQN6_MU7msaSbPppXoQVi_msNnt3ae70YE9skOkPfT_Ofefv_AE0JrwAnKYt-GEhHymIGYGNnJPeFSHk6rLyZ3xNIGfHchikwpLhrnNvMiwEIJXnkVKLQGqRNC5jxt1Jgld2N5EfDiWFIvu3LYhXMp-Sxm0sYoqH_cXAo3M1RUl9IceGnN6HDvedBYykVuOnBh-ykhEjYkoFusGuk3pGBB-npdMi0I-g4alxvX197garyr_dj0mmtk9DMRETVSIL_D4LG1WsCRQyrDFnQ_x3UdZfPfkQTOL8-C9axKiOhQa6otbijqaEwTgZEXCFVsICD_DxIy-dGOyMl0UhtMXV9zCKbpzupbb81blSxuXb2PwBBG0v4
 "Event Flow Diagram")

## Getting Started 🏃

### 1. Clone & Install Dependencies

You can choose between the traditional `python -m venv` approach **or** the blazing-fast [`uv`](https://github.com/astral-sh/uv) tool (written in Rust):

<details>
<summary>Option A – Standard <code>venv + pip</code></summary>

```bash
python -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate
pip install -r requirements.txt
```

</details>

<details>
<summary>Option B – Super-fast <code>uv</code> (creates env & installs deps)</summary>

Install `uv` once globally (if not already):

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```

Then, inside the project root:

```bash
uv venv  # creates .venv by default
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

`uv` acts as a drop-in replacement for `pip`, while being much faster and creating deterministic lockfiles (`uv pip compile`). Feel free to use whichever workflow you prefer.

</details>

### 2. Start Kafka with Docker Compose

```bash
docker compose up -d  # spins up Zookeeper, Kafka, and Kafdrop UI
```

*Visit <http://localhost:19000> to inspect topics in Kafdrop.*

> **What is Kafdrop?**  
> Kafdrop is a lightweight web UI that lets you browse topics, partitions, and the latest messages without using Kafka CLI tools. It’s included only for convenience during demos and local development.  
> If you prefer a slimmer stack you can remove the entire `kafdrop` service block from `docker-compose.yml` and Kafka + Zookeeper will run just fine.

### 3. Run the FastAPI Producer

```bash
uvicorn main:app --reload
```

Send a test message:

```bash
curl -X POST http://127.0.0.1:8000/publish \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello, Kafka!"}'
```

### 4. Start the Consumer

```bash
python consumer.py
```

You should see the message printed in the consumer terminal:

```text
Consumed → partition=0 offset=0 value={'message': 'Hello, Kafka!'}
```

## Customisation

* **Topic name** – set `TOPIC_NAME` env var on producer/consumer.
* **Bootstrap servers** – set `KAFKA_BOOTSTRAP_SERVERS` (Defaults to `localhost:9092`).

## Cleaning Up 🧹

```bash
docker compose down -v  # stops containers and removes volumes
```

---

### Further Reading

* [Kafka Documentation](https://kafka.apache.org/documentation/)
* [FastAPI Docs](https://fastapi.tiangolo.com/)
* [aiokafka](https://github.com/aio-libs/aiokafka)

Enjoy your journey into event-driven architectures! ✨
