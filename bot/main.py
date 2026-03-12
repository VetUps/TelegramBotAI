import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import config
from app.handlers import common, games, sentiment, ai_chat
from app.services.ml_service.ml_client import MlClient
from app.services.ml_service.config import Config as MlConfig

async def main():
    logging.basicConfig(level=logging.INFO)
    
    ml_config = MlConfig()
    ml_client = MlClient(ml_config)
    await ml_client.connect()
    
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher(ml_client=ml_client)
    
    dp.include_router(common.router)
    dp.include_router(games.router)
    dp.include_router(sentiment.router)
    dp.include_router(ai_chat.router)
    
    print("🚀 Бот запущен с интеграцией RabbitMQ!")
    
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await ml_client.close()
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())