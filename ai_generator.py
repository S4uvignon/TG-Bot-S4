import google.generativeai as genai
import os
from config import GOOGLE_API_KEY
from prompts import get_prompt

# Инициализация Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

async def generate_telegram_post(vacancy_info: str):
    """Генерирует текст поста и промпт для картинки"""
    prompt_template = get_prompt()
    
    # Добавляем инструкцию для генерации промпта к картинке
    full_instruction = f"""
    {prompt_template.format(vacancy_info=vacancy_info)}
    
    ВАЖНО: В самом конце ответа, после текста поста, добавь строку:
    IMAGE_PROMPT: [напиши здесь короткий английский промпт для генерации обложки вакансии в стиле 3D render или flat design]
    """
    
    response = model.generate_content(full_instruction)
    full_text = response.text
    
    # Разделяем текст поста и промпт для картинки
    if "IMAGE_PROMPT:" in full_text:
        post_part, image_prompt = full_text.split("IMAGE_PROMPT:", 1)
        return post_part.strip(), image_prompt.strip()
    
    return full_text.strip(), "Professional office workspace, 3D render, minimalist"

async def generate_image(prompt: str) -> str:
    """Генерирует изображение (Nano Banana / Imagen)"""
    # Используем ту же модель Gemini для генерации (в Free Tier AI Studio)
    # Если у тебя настроен Google Cloud Vertex AI, здесь вызывается ImageGenerationModel
    # Для базовой версии через API AI Studio пока используем заглушку или простую логику:
    import asyncio
    await asyncio.sleep(1) # Имитация работы
    return None # Вернем None, если API Nano Banana еще не подключено в GCP
