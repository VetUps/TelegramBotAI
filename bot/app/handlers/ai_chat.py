from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from app.states.fsm import BotStates
from app.keyboards.inline import get_ai_models_keyboard, get_ai_type_keyboard
from app.services.ai_client import ask_ai
from aiogram.types import BufferedInputFile
from app.services.media_client import generate_image_bytes, generate_video_bytes

router = Router()

# ================= 1. ГЛАВНОЕ МЕНЮ ИИ =================
@router.message(F.text == "🤖 ИИ")
async def ai_menu(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Что вы хотите сгенерировать?", reply_markup=get_ai_type_keyboard())

# ================= 2. ОБРАБОТКА ВЫБОРА ТИПА =================
@router.callback_query(F.data.startswith("type_"))
async def ai_type_selected(callback: types.CallbackQuery, state: FSMContext):
    selected_type = callback.data.replace("type_", "") # text, image или video
    
    if selected_type == "text":
        # Если текст - показываем старое меню с выбором моделей
        await callback.message.edit_text("С какой нейросетью хотите пообщаться?", reply_markup=get_ai_models_keyboard())
    
    elif selected_type == "image":
        await state.set_state(BotStates.ai_image_mode)
        await callback.message.edit_text("🖼️ **Режим: Генерация фото (Qwen)**\nОтправьте подробное описание того, что хотите увидеть:", parse_mode="Markdown")
    
    elif selected_type == "video":
        await state.set_state(BotStates.ai_video_mode)
        await callback.message.edit_text("🎬 **Режим: Генерация видео (Wan)**\nОтправьте промпт для видео. Учтите, рендер займет 2-10 минут:", parse_mode="Markdown")
        
    await callback.answer()

# ================= 3. ГЕНЕРАЦИЯ ТЕКСТА (Старая логика) =================
@router.callback_query(F.data.startswith("model_"))
async def ai_model_selected(callback: types.CallbackQuery, state: FSMContext):
    selected_model = callback.data.replace("model_", "")
    await state.update_data(ai_model=selected_model)
    await state.set_state(BotStates.ai_chat_mode)
    
    await callback.message.edit_text(f"✅ Вы подключились к **{selected_model.upper()}**.\nНапишите ваш запрос:", parse_mode="Markdown")
    await callback.answer()

@router.message(BotStates.ai_chat_mode)
async def ai_chat_process(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    model = user_data.get("ai_model", "qwen")
    
    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
    response = await ask_ai(message.text, model)
    await message.answer(f"[{model.upper()}]:\n{response}", parse_mode="Markdown")

# ================= 4. ГЕНЕРАЦИЯ ФОТО =================
@router.message(BotStates.ai_image_mode)
async def ai_image_process(message: types.Message, state: FSMContext):
    await message.answer("⏳ Отправил задачу художнику. Ждем...")
    await message.bot.send_chat_action(chat_id=message.chat.id, action="upload_photo")
    
    result = await generate_image_bytes(message.text)
    
    if isinstance(result, str) and result.startswith("error:"):
        await message.answer(f"❌ Произошла ошибка: {result}")
    else:
        # Оборачиваем байты в BufferedInputFile для отправки
        photo_file = BufferedInputFile(result, filename="generated_image.png")
        await message.answer_photo(photo=photo_file, caption=f"✨ Готово по запросу: {message.text}")

# ================= 5. ГЕНЕРАЦИЯ ВИДЕО =================
@router.message(BotStates.ai_video_mode)
async def ai_video_process(message: types.Message, state: FSMContext):
    await message.answer("🔄 Задача на видео принята в очередь. Обычно это занимает от 5 до 10 минут. Я пришлю результат, как только он будет готов! Можете пока пользоваться другими функциями бота.")
    
    result = await generate_video_bytes(message.text)
    
    if isinstance(result, str) and result.startswith("error:"):
        await message.answer(f"❌ Ошибка при генерации видео: {result}")
    else:
        # Оборачиваем байты в BufferedInputFile
        video_file = BufferedInputFile(result, filename="generated_video.mp4")
        await message.answer_video(video=video_file, caption=f"🎬 Ваше видео по запросу: {message.text}")