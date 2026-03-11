import asyncio
import logging
from aiogram import Bot, Dispatcher

                                   
from config import config

                                               
from app.handlers import common, games, sentiment, ai_chat

async def main():
                                                                                               
    logging.basicConfig(level=logging.INFO)
    
                                     
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()
    
                                       
                                                                            
    dp.include_router(common.router)
    dp.include_router(games.router)
    dp.include_router(sentiment.router)
    dp.include_router(ai_chat.router)
    
    print("🚀 Бот успешно запущен и готов к работе!")
    
    try:
                                                                     
                                                                                                              
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
                                                               
        await bot.session.close()

if __name__ == "__main__":
                                        
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Бот остановлен вручную.")