from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from app.states.fsm import BotStates

router = Router()

@router.message(F.text == "📊 Классификация тональности")
async def sentiment_start(message: types.Message, state: FSMContext):
    await state.set_state(BotStates.waiting_for_sentiment_text)
    await message.answer("Отправьте любой текст (например, комментарий), и моя ML-модель оценит его тональность:")

@router.message(BotStates.waiting_for_sentiment_text)
async def sentiment_analyze(message: types.Message, state: FSMContext):
    text_to_analyze = message.text
    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
    
                                                                            
    await message.answer(f"🧠 Результат анализа для:\n«{text_to_analyze}»\n\n*(Тут будет ответ от трансформера)*")
    
    await state.clear()