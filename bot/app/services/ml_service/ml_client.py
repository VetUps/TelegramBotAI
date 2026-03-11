import asyncio
import json
import uuid

import aio_pika
import aio_pika.abc

from config import Config


class QueueAdapter:
    def __init__(self, config: Config):
        self.host = config.RABBITMQ_HOST
        self.port = config.RABBITMQ_PORT
        self.user = config.RABBITMQ_DEFAULT_USER
        self.password = config.RABBITMQ_DEFAULT_PASS

        self.request_queue = "requests_queue"
        self.response_queue = "results_queue"

        self.connection: aio_pika.abc.AbstractConnection | None = None
        self.channel: aio_pika.abc.AbstractChannel | None = None

                                                                   
        self._pending: dict[str, asyncio.Future] = {}

    async def connect(self):
        """Устанавливает соединение и запускает прослушивание результатов"""
        self.connection = await aio_pika.connect_robust(
            host=self.host,
            port=self.port,
            login=self.user,
            password=self.password,
        )
        self.channel = await self.connection.channel()
        await self.channel.declare_queue(self.request_queue)
        await self.channel.declare_queue(self.response_queue)

                                                               
        response_queue = await self.channel.get_queue(self.response_queue)
        await response_queue.consume(self._on_response)

    async def _on_response(self, message: aio_pika.abc.AbstractIncomingMessage):
        """
        Коллбэк для входящих результатов.
        Находит Future по correlation_id и кладёт в него результат
        """
        async with message.process():
            correlation_id = message.correlation_id
            if correlation_id in self._pending:
                result = json.loads(message.body.decode())
                self._pending[correlation_id].set_result(result)
            else:
                print(f"Неизвестный correlation_id: {correlation_id}, пропускаем")

    async def send_message(self, text: str, model: str = "base_bert") -> dict:
        """
        Отправляет текст на классификацию и ожидает результат.

        :param text: текст для классификации
        :param model: модель классификатора
        :return: результат классификации
        """
        correlation_id = str(uuid.uuid4())

        loop = asyncio.get_event_loop()
        future: asyncio.Future = loop.create_future()
        self._pending[correlation_id] = future

        await self.channel.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps({"text": text, "model": model}).encode(),
                correlation_id=correlation_id,
                reply_to=self.response_queue,
                content_type="application/json",
            ),
            routing_key=self.request_queue,
        )

        try:
            return await asyncio.wait_for(future, timeout=30)
        except asyncio.TimeoutError:
            raise TimeoutError("ML-сервис не ответил за 30 секунд")
        finally:
            self._pending.pop(correlation_id, None)

    async def close(self):
        if self.channel and not self.channel.is_closed:
            await self.channel.close()
        if self.connection and not self.connection.is_closed:
            await self.connection.close()


class MlClient:
    def __init__(self, config: Config):
        self.adapter = QueueAdapter(config)

    async def connect(self):
        await self.adapter.connect()

    async def classify(self, text: str, model: str = "base_bert") -> dict:
        return await self.adapter.send_message(text, model)

    async def close(self):
        await self.adapter.close()


async def main():
    config = Config()
    client = MlClient(config)
    await client.connect()
    result = await client.classify("Хотел бы полизать твою попочку")
    print(result)
    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
