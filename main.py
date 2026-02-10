import asyncio
import logging
from aiogram import Bot
from bot import dp
from config import TELEGRAM_BOT_TOKEN

async def main():
    logging.basicConfig(level=logging.INFO)
    
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    
    # Обязательно удаляем вебхуки, чтобы работал polling
    await bot.delete_webhook(drop_pending_updates=True)
    
    print("🚀 Бот запускается на Amvera...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
