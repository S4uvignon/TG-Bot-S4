from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from config import TELEGRAM_BOT_TOKEN
from hh_api import extract_vacancy_id, get_vacancy_info, format_vacancy_data
from ai_generator import generate_telegram_post


dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "👋 Привет! Я бот для создания постов о вакансиях.\n\n"
        "Отправь мне ссылку на вакансию с hh.ru, и я создам готовый пост для твоего Telegram-канала.\n\n"
        "Пример: https://hh.ru/vacancy/12345678"
    )


@dp.message(F.text.contains("hh.ru"))
async def process_vacancy_link(message: Message):
    # Извлекаем ID вакансии
    vacancy_id = extract_vacancy_id(message.text)
    
    if not vacancy_id:
        await message.answer("❌ Не удалось извлечь ID вакансии из ссылки. Проверьте формат.")
        return
    
    await message.answer("⏳ Обрабатываю вакансию...")
    
    # Получаем данные с HH API
    vacancy_data = await get_vacancy_info(vacancy_id)
    
    if not vacancy_data:
        await message.answer("❌ Не удалось получить данные о вакансии. Проверьте ссылку.")
        return
    
    # Форматируем данные
    formatted_data = format_vacancy_data(vacancy_data)
    
    # Генерируем пост через AI
    try:
        post = await generate_telegram_post(formatted_data)
        await message.answer(f"✅ Готовый пост:\n\n{post}")
    except Exception as e:
        await message.answer(f"❌ Ошибка при генерации поста: {str(e)}")


@dp.message()
async def unknown_message(message: Message):
    await message.answer(
        "Пожалуйста, отправьте ссылку на вакансию с hh.ru\n"
        "Например: https://hh.ru/vacancy/12345678"
    )