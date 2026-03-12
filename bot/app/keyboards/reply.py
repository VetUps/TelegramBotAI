from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Генерирует главное Reply-меню бота."""
    builder = ReplyKeyboardBuilder()
    
                                    
    builder.button(text="🎮 Скидки на игры")
    builder.button(text="🤖 ИИ")
    builder.button(text="📊 Классификация тональности")
    builder.button(text="ℹ️ Справка")
    builder.button(text="❌ Выход")
    
                                        
                     
                          
                           
    builder.adjust(2, 1, 2)
    
                                                                       
    return builder.as_markup(
        resize_keyboard=True, 
        input_field_placeholder="Выберите функцию..."
    )