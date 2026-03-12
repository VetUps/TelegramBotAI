import json
import time
from typing import Dict
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import pika
from pika.spec import BasicProperties

from classifier import Classifier
from config import Config

try:
    app_config = Config()
    app_config.validate()
    print("Конфигурационные данные загружены")
except Exception as e:
    print(f"Ошибка инициализации конфигурационных данных: {e}")
    exit(1)


def init_classifiers() -> Dict[str, Classifier]:
    bert_basic_tokenizer = AutoTokenizer.from_pretrained("VetUps/final_tokenizer")
    bert_basic_model = AutoModelForSequenceClassification.from_pretrained(
        "VetUps/final_model"
    )
    bert_basic_classifier = Classifier(bert_basic_model, bert_basic_tokenizer)

    bert_pavlov_tokenizer = AutoTokenizer.from_pretrained("VetUps/pavlov-bert")
    bert_pavlov_model = AutoModelForSequenceClassification.from_pretrained(
        "VetUps/pavlov-bert"
    )
    bert_pavlov_classifier = Classifier(bert_pavlov_model, bert_pavlov_tokenizer)

    return {
        "base_bert": bert_basic_classifier,
        "pavlov_bert": bert_pavlov_classifier,
    }


def make_callback(channel: pika.channel.Channel, classifiers: Dict[str, Classifier]):
    """
    Прокидывает channel и classifiers через замыкание,
    чтобы не использовать глобальные переменные
    """

    def callback(ch, method, properties: BasicProperties, body: bytes):
        try:
            message = json.loads(body.decode())
        except json.JSONDecodeError as e:
            print(f"Не удалось распарсить сообщение: {e}")
            return

        text = message.get("text")
        model_name = message.get("model", "base_bert")

        if not text:
            print("Сообщение не содержит поле 'text', пропускаем")
            return

        classifier = classifiers.get(model_name)
        if classifier is None:
            print(
                f"Неизвестная модель: {model_name}, доступны: {list(classifiers.keys())}"
            )
            return

        try:
            result = classifier.predict(text)
        except Exception as e:
            print(f"Ошибка классификации: {e}")
            return

        reply_queue = properties.reply_to or "results_queue"

        response = {
            "model": model_name,
            "result": result,
                                                            
            "correlation_id": properties.correlation_id,
        }

        channel.basic_publish(
            exchange="",
            routing_key=reply_queue,
            body=json.dumps(response, ensure_ascii=False),
            properties=pika.BasicProperties(
                correlation_id=properties.correlation_id,
                content_type="application/json",
            ),
        )

        print(f"Результат отправлен в '{reply_queue}': {response}")

    return callback


def start_consuming(classifiers: Dict[str, Classifier]):
    credentials = pika.PlainCredentials(
        username=app_config.RABBITMQ_DEFAULT_USER,
        password=app_config.RABBITMQ_DEFAULT_PASS,
    )
    connection_params = pika.ConnectionParameters(
        host=app_config.RABBITMQ_HOST,
        port=app_config.RABBITMQ_PORT,
        credentials=credentials,
    )

    for attempt in range(5):
        try:
            connection = pika.BlockingConnection(connection_params)
            break
        except pika.exceptions.AMQPConnectionError:
            print(f"Попытка подключения {attempt + 1}/5...")
            time.sleep(3)
    else:
        print("Не удалось подключиться к RabbitMQ")
        exit(1)

    channel = connection.channel()
    channel.queue_declare(queue="requests_queue")
    channel.queue_declare(queue="results_queue")

    channel.basic_consume(
        queue="requests_queue",
        auto_ack=True,
        on_message_callback=make_callback(channel, classifiers),
    )

    print("Ожидание сообщений")
    channel.start_consuming()


if __name__ == "__main__":
    print("Загрузка моделей")
    classifiers = init_classifiers()
    print("Модели загружены, запускаем консьюмер")
    start_consuming(classifiers)
