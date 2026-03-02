from openai import OpenAI
from config import GROQ_API_KEY, GROQ_BASE_URL
from prompts import get_prompt

GROQ_BASE_URL = "https://api.groq.com/openai/v1"

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
    
    return response.choices[0].message.content
