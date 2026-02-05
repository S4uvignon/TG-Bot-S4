from openai import OpenAI
from config import GROQ_API_KEY, GROQ_BASE_URL


async def generate_telegram_post(vacancy_info: str) -> str:
    """Генерирует пост для Telegram на основе информации о вакансии"""
    
    client = OpenAI(
        api_key=GROQ_API_KEY,
        base_url=GROQ_BASE_URL
    )
    
    prompt = f"""
На основе следующей информации о вакансии создай привлекательный пост для Telegram-канала о работе.

Требования к посту:
- Используй эмодзи для визуального оформления
- Выдели ключевые преимущества вакансии
- Сделай акцент на зарплате (если указана)
- Добавь призыв к действию
- Длина поста: 150-300 слов
- Тон: профессиональный, но дружелюбный

Информация о вакансии:
{vacancy_info}

Создай готовый пост:
"""
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # Быстрая и качественная модель
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
