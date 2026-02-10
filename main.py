import asyncio
import logging
from aiohttp import web
from aiogram import Bot
from bot import dp
from config import TELEGRAM_BOT_TOKEN


# Простой HTTP сервер для Health Check
async def health_check(request):
    return web.Response(text="Bot is running! 🤖")


async def start_web_server():
    """Запускает HTTP сервер на порту 10000 для Render"""
    app = web.Application()
    app.router.add_get('/', health_check)
    app.router.add_get('/health', health_check)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 10000)
    await site.start()
    print("✅ Web server started on port 10000")


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    
    # Удаляем webhook перед запуском polling
    await bot.delete_webhook(drop_pending_updates=True)
    
    print("✅ Бот запущен!")
    
    # Запускаем веб-сервер в фоне (для Render Health Check)
    asyncio.create_task(start_web_server())
    
    # Запускаем бота
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
