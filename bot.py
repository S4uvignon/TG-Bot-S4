from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.enums import ParseMode
from config import TELEGRAM_BOT_TOKEN, ADMIN_IDS
from hh_api import extract_vacancy_id, get_vacancy_info, format_vacancy_data
from ai_generator import generate_telegram_post
from prompts import get_prompt, set_prompt, reset_prompt
from hh_api import extract_vacancy_id, get_vacancy_info, format_vacancy_data



dp = Dispatcher()


# Состояния для FSM (конечный автомат)
class PromptEdit(StatesGroup):
    waiting_for_prompt = State()


# Проверка, является ли пользователь администратором
def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


@dp.message(Command("start"))
async def cmd_start(message: Message):
    keyboard = None
    
    # Если пользователь - админ, показываем кнопку настроек
    if is_admin(message.from_user.id):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⚙️ Настройки промпта", callback_data="settings")]
        ])
    
    await message.answer(
        "👋 Привет! Я бот для создания постов о вакансиях.\n\n"
        "Отправь мне ссылку на вакансию с hh.ru, и я создам готовый пост для твоего Telegram-канала.\n\n"
        "Пример: https://hh.ru/vacancy/12345678",
        reply_markup=keyboard
    )


@dp.callback_query(F.data == "settings")
async def show_settings(callback: CallbackQuery):
    # Проверка прав администратора
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ У вас нет доступа к этой функции", show_alert=True)
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Изменить промпт", callback_data="edit_prompt")],
        [InlineKeyboardButton(text="👁 Посмотреть текущий промпт", callback_data="view_prompt")],
        [InlineKeyboardButton(text="🔄 Сбросить к дефолтному", callback_data="reset_prompt")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_start")]
    ])
    
    await callback.message.edit_text(
        "⚙️ *Настройки промпта*\n\n"
        "Выберите действие:",
        parse_mode="Markdown",
        reply_markup=keyboard
    )
    await callback.answer()


@dp.callback_query(F.data == "view_prompt")
async def view_prompt(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ У вас нет доступа к этой функции", show_alert=True)
        return
    
    current_prompt = get_prompt()
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Назад", callback_data="settings")]
    ])
    
    await callback.message.edit_text(
        f"📄 *Текущий промпт:*\n\n```\n{current_prompt}\n```\n\n"
        "В промпте используйте `{{vacancy_info}}` для подстановки данных о вакансии.",
        parse_mode="Markdown",
        reply_markup=keyboard
    )
    await callback.answer()


@dp.callback_query(F.data == "edit_prompt")
async def edit_prompt(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ У вас нет доступа к этой функции", show_alert=True)
        return
    
    await callback.message.edit_text(
        "✏️ *Редактирование промпта*\n\n"
        "Отправьте новый промпт текстовым сообщением.\n\n"
        "⚠️ Обязательно используйте `{vacancy_info}` в тексте - туда будут подставляться данные о вакансии.\n\n"
        "Для отмены отправьте /cancel",
        parse_mode="Markdown"
    )
    await callback.answer()
    await state.set_state(PromptEdit.waiting_for_prompt)


@dp.message(PromptEdit.waiting_for_prompt)
async def save_new_prompt(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("❌ У вас нет доступа к этой функции")
        await state.clear()
        return
    
    new_prompt = message.text
    
    # Проверяем наличие {vacancy_info}
    if "{vacancy_info}" not in new_prompt:
        await message.answer(
            "❌ Ошибка! Промпт должен содержать `{vacancy_info}`\n\n"
            "Попробуйте еще раз или отправьте /cancel для отмены.",
            parse_mode="Markdown"
        )
        return
    
    # Сохраняем новый промпт
    set_prompt(new_prompt)
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ К настройкам", callback_data="settings")]
    ])
    
    await message.answer(
        "✅ Промпт успешно обновлен!\n\n"
        f"📝 Новый промпт:\n```\n{new_prompt[:200]}{'...' if len(new_prompt) > 200 else ''}\n```",
        parse_mode="Markdown",
        reply_markup=keyboard
    )
    await state.clear()


@dp.callback_query(F.data == "reset_prompt")
async def reset_prompt_callback(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ У вас нет доступа к этой функции", show_alert=True)
        return
    
    reset_prompt()
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ К настройкам", callback_data="settings")]
    ])
    
    await callback.message.edit_text(
        "✅ Промпт сброшен к дефолтному значению!",
        reply_markup=keyboard
    )
    await callback.answer()


@dp.callback_query(F.data == "back_to_start")
async def back_to_start(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚙️ Настройки промпта", callback_data="settings")]
    ])
    
    await callback.message.edit_text(
        "👋 Привет! Я бот для создания постов о вакансиях.\n\n"
        "Отправь мне ссылку на вакансию с hh.ru, и я создам готовый пост для твоего Telegram-канала.\n\n"
        "Пример: https://hh.ru/vacancy/12345678",
        reply_markup=keyboard
    )
    await callback.answer()


@dp.message(Command("cancel"))
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("Нечего отменять")
        return
    
    await state.clear()
    await message.answer("❌ Действие отменено")


@dp.message(F.text.contains("hh.ru"))
async def process_vacancy_link(message: Message):
    vacancy_id = extract_vacancy_id(message.text)
    if not vacancy_id:
        await message.answer("❌ Не удалось извлечь ID вакансии.")
        return
    
    original_url = message.text.strip()
    status_msg = await message.answer("⏳ Генерирую пост и обложку...")
    
    vacancy_data = await get_vacancy_info(vacancy_id)
    if not vacancy_data:
        await status_msg.edit_text("❌ Ошибка получения данных с HH.")
        return
    
    formatted_data = format_vacancy_data(vacancy_data, original_url)  # ← ИСПРАВЛЕНО
    
    try:
        # Безопасная распаковка результата
        result = await generate_telegram_post(formatted_data)
        logger.info(f"Результат: {type(result)}")
        
        if isinstance(result, tuple) and len(result) == 2:
            post_text, img_prompt = result
        elif isinstance(result, str):
            post_text = result
            img_prompt = "Professional workspace"
        else:
            raise ValueError(f"Неожиданный результат: {result}")
        
        footer = f"\n\n<b><a href=\"{original_url}\">👉🏻 ссылка на вакансию</a></b>"
        full_post = post_text + footer
        
        await message.answer_photo(
            photo="https://placehold.co/600x400/png?text=Vacancy+Image",
            caption=full_post,
            parse_mode="HTML"
        )
        await status_msg.delete()
        
    except Exception as e:
        logger.error(f"Ошибка: {e}", exc_info=True)
        await status_msg.edit_text(f"❌ Ошибка: {str(e)}")


@dp.message()
async def unknown_message(message: Message):
    await message.answer(
        "Пожалуйста, отправьте ссылку на вакансию с hh.ru\n"
        "Например: https://hh.ru/vacancy/12345678"
    )
