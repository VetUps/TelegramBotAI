from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_ai_type_keyboard() -> InlineKeyboardMarkup:
    """Генерирует меню для выбора типа контента."""
    builder = InlineKeyboardBuilder()
    builder.button(text="📝 Текст", callback_data="type_text")
    builder.button(text="🖼️ Фото (Qwen)", callback_data="type_image")
    builder.button(text="🎬 Видео (Qwen)", callback_data="type_video")
    builder.adjust(1) # В один столбик
    return builder.as_markup()

def get_ai_models_keyboard() -> InlineKeyboardMarkup:
    """Генерирует меню для выбора текстовой нейросети."""
    builder = InlineKeyboardBuilder()
    builder.button(text="🧠 Qwen (Alibaba)", callback_data="model_qwen")
    builder.button(text="🐳 DeepSeek", callback_data="model_deepseek")
    builder.button(text="✨ Gemini (Google)", callback_data="model_gemini")
    builder.adjust(1)
    return builder.as_markup()