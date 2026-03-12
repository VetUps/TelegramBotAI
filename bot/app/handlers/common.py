from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from app.keyboards.reply import get_main_keyboard

                                 
router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
                                                 
    await state.clear()
    await message.answer(
        "Привет! Я ваш универсальный бот на микросервисах 🚀\n"
        "Выберите нужное действие в меню:",
        reply_markup=get_main_keyboard()
    )

@router.message(F.text == "ℹ️ Справка")
async def process_help(message: types.Message):
    text = (
        "📖 **Что я умею:**\n\n"
        "🎮 **Скидки на игры** - найду лучшую цену по всем магазинам.\n"
        "🤖 **ИИ** - пообщаюсь с вами через Qwen, DeepSeek или Gemini.\n"
        "📊 **Классификация** - оценю тональность вашего текста.\n"
        "❌ **Выход** - закрою меню."
    )
    await message.answer(text, parse_mode="Markdown")

@router.message(F.text == "❌ Выход")
async def process_exit(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Сеанс завершен. Клавиатура скрыта.\nНапишите /start, чтобы вернуть меню.", 
        reply_markup=types.ReplyKeyboardRemove()
    )