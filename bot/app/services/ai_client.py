from openai import AsyncOpenAI
import google.generativeai as genai
from config import config

qwen_client = AsyncOpenAI(
    api_key=config.QWEN_API,
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
)

deepseek_client = AsyncOpenAI(
    api_key=config.DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com/v1"
)

genai.configure(api_key=config.GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-1.5-pro')

async def ask_ai(prompt: str, model_choice: str = "qwen") -> str:
    """
    Отправляет запрос к выбранной нейросети и возвращает текст.
    model_choice может быть: 'qwen', 'deepseek', 'gemini'
    """
    try:
        if model_choice == "qwen":
            response = await qwen_client.chat.completions.create(
                model="qwen-plus",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content

        elif model_choice == "deepseek":
            response = await deepseek_client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content

        elif model_choice == "gemini":
            response = await gemini_model.generate_content_async(prompt)
            return response.text

        else:
            return "❌ Выбрана неизвестная модель ИИ."

    except Exception as e:
        print(f"Ошибка при обращении к {model_choice}: {e}")
        return f"⚠️ Ошибка сети при запросе к {model_choice.capitalize()}."