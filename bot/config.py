import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    
    # Ключи для нейросетей
    QWEN_API = os.getenv("QWEN_API")
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # Внутренние сервисы
    ML_SERVICE_URL = os.getenv("ML_SERVICE_URL", "http://ml-service:8000")

config = Config()