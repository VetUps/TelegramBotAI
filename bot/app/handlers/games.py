from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from app.states.fsm import BotStates
from app.services.games_client import get_game_discount

router = Router()

@router.message(F.text == "🎮 Скидки на игры")
async def games_start(message: types.Message, state: FSMContext):
                                                   
    await state.set_state(BotStates.waiting_for_game_name)
    await message.answer("Напишите название игры, которую ищем (например, Satisfactory или Cyberpunk):")

                                                                                    
@router.message(BotStates.waiting_for_game_name)
async def games_search(message: types.Message, state: FSMContext):
    game_name = message.text
    
                                                          
    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
    
                  
    result = await get_game_discount(game_name)
    await message.answer(f"🔍 Ищу лучшие цены на **{game_name}**...\n{result}", parse_mode="Markdown")
    
                                                                    
    await state.clear()