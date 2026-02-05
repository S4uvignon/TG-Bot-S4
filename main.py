import asyncio
import logging
from aiogram import Bot
from bot import dp
from config import TELEGRAM_BOT_TOKEN


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    
    print("Бот запущен!")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())