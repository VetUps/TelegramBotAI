from typing import Dict
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import pika

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
    """
    Инициализирует модели
    :return:
    """
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


def callback(ch, method, properties, body):
    print(f"Получено сообщение {body.decode()}")


def start_consuming():
    credentials = pika.PlainCredentials(
        username=app_config.RABBITMQ_DEFAULT_USER,
        password=app_config.RABBITMQ_DEFAULT_PASS,
    )
    connection_params = pika.ConnectionParameters(
        host=app_config.RABBITMQ_HOST,
        port=app_config.RABBITMQ_PORT,
        credentials=credentials,
    )
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    channel.queue_declare(queue="requests_queue")
    channel.basic_consume(
        queue="requests_queue",
        auto_ack=True,
        on_message_callback=callback,
    )
    channel.start_consuming()


if __name__ == "__main__":
    start_consuming()
