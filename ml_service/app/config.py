import os
from dotenv import load_dotenv


class Config:
    """Класс конфигурации с валидацией"""

    def __init__(self):
        load_dotenv()

        self.RABBITMQ_HOST: str = os.getenv("RABBITMQ_HOST")
        self.RABBITMQ_DEFAULT_USER: str = os.getenv("RABBITMQ_DEFAULT_USER")
        self.RABBITMQ_DEFAULT_PASS: str = os.getenv("RABBITMQ_DEFAULT_PASS")
        self.RABBITMQ_PORT: str = os.getenv("RABBITMQ_PORT")

    def validate(self):
                                               
        if not self.RABBITMQ_HOST:
            raise ValueError("В env не указана переменная: RABBITMQ_HOST")
        if not self.RABBITMQ_DEFAULT_USER:
            raise ValueError("В env не указана переменная: RABBITMQ_DEFAULT_USER")
        if not self.RABBITMQ_DEFAULT_PASS:
            raise ValueError("В env не указана переменная: RABBITMQ_DEFAULT_PASS")
        if not self.RABBITMQ_PORT:
            raise ValueError("В env не указана переменная: RABBITMQ_PORT")
