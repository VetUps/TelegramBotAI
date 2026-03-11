from aiogram.fsm.state import State, StatesGroup

class BotStates(StatesGroup):
    # --- Режим: Скидки на игры ---
    # Бот ждет, пока пользователь напишет название игры (например, "Cyberpunk 2077")
    waiting_for_game_name = State()
    
    # --- Режим: Общение с ИИ ---
    # Бот находится в режиме диалога с выбранной нейросетью
    ai_chat_mode = State()           # Для генерации текста
    ai_image_mode = State()          # Для генерации фото
    ai_video_mode = State()          # Для генерации видео
    
    # --- Режим: Классификация тональности ---
    # Бот ждет текст, чтобы отправить его в ваш ML-микросервис
    waiting_for_sentiment_text = State()