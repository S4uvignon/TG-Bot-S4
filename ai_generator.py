from openai import OpenAI
import os
from config import GROQ_API_KEY, GROQ_BASE_URL
from prompts import get_prompt

async def generate_telegram_post(vacancy_info: str) -> str:
    """Генерирует пост для Telegram через Groq (Llama 3.3)"""
    
    # Инициализируем клиента
    client = OpenAI(
        api_key=GROQ_API_KEY,
        base_url=GROQ_BASE_URL
    )
    
    # Получаем промпт
    prompt_template = get_prompt()
    prompt = prompt_template.format(vacancy_info=vacancy_info)
    
    # Запрос к Groq
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system", 
                "content": "Ты профессиональный HR-копирайтер. Пиши на русском языке, используя HTML-разметку."
            },
            {
                "role": "user", 
                "content": prompt
            }
        ],
        max_tokens=1000,
        temperature=0.7
    )
    
    return response.choices[0].message.content
