import asyncio
import logging
from aiogram import Bot, Dispatcher

# Импортируем наш конфиг с токенами
from config import config

# Импортируем все роутеры из наших обработчиков
from app.handlers import common, games, sentiment, ai_chat

async def main():
    # Включаем логирование, чтобы видеть в консоли, что происходит (ошибки, входящие сообщения)
    logging.basicConfig(level=logging.INFO)
    
    # Инициализируем бота и диспетчер
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()
    
    # Регистрируем роутеры в диспетчере
    # Порядок имеет значение! Базовые команды (common) лучше ставить первыми
    dp.include_router(common.router)
    dp.include_router(games.router)
    dp.include_router(sentiment.router)
    dp.include_router(ai_chat.router)
    
    print("🚀 Бот успешно запущен и готов к работе!")
    
    try:
        # Запускаем постоянный опрос серверов Telegram (Long Polling)
        # Бот будет игнорировать старые сообщения, которые пришли, пока он был выключен (drop_pending_updates)
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        # Корректно закрываем сессию бота при остановке скрипта
        await bot.session.close()

if __name__ == "__main__":
    # Запускаем асинхронную функцию main
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Бот остановлен вручную.")