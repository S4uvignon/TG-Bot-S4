from openai import OpenAI
from config import GROQ_API_KEY, GROQ_BASE_URL
from prompts import get_prompt
from typing import Optional


async def generate_telegram_post(vacancy_info: str) -> str:
    """Генерирует пост для Telegram на основе информации о вакансии"""
    
    client = OpenAI(
        api_key=GROQ_API_KEY,
        base_url=GROQ_BASE_URL
    )
    
    # Получаем текущий промпт и подставляем информацию о вакансии
    prompt_template = get_prompt()
    prompt = prompt_template.format(vacancy_info=vacancy_info)
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system", 
                "content": "Ты помощник, который создаёт привлекательные посты для Telegram-канала о работе. Пиши на русском языке."
            },
            {
                "role": "user", 
                "content": prompt
            }
        ],
        max_tokens=1000,
        temperature=0.7
    )
    
    generated_post = response.choices[0].message.content
    
    # Добавляем ссылку в конец поста, если она не была добавлена нейросетью
    if vacancy_url and vacancy_url not in generated_post:
        generated_post += f"\n\n🔗 Ссылка на вакансию: {vacancy_url}"
    
    return generated_post
