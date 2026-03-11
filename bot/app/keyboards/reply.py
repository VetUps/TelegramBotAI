from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Генерирует главное Reply-меню бота."""
    builder = ReplyKeyboardBuilder()
    
    # Добавляем наши основные кнопки
    builder.button(text="🎮 Скидки на игры")
    builder.button(text="🤖 ИИ")
    builder.button(text="📊 Классификация тональности")
    builder.button(text="ℹ️ Справка")
    builder.button(text="❌ Выход")
    
    # Красиво распределяем их по рядам: 
    # 1 ряд: Игры, ИИ
    # 2 ряд: Классификация
    # 3 ряд: Справка, Выход
    builder.adjust(2, 1, 2)
    
    # resize_keyboard=True делает кнопки аккуратными (не на пол-экрана)
    return builder.as_markup(
        resize_keyboard=True, 
        input_field_placeholder="Выберите функцию..."
    )