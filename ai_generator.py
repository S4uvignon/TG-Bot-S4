from anthropic import Anthropic
from config import ANTHROPIC_API_KEY

# Для OpenAI используйте:
# from openai import OpenAI
# client = OpenAI(api_key=OPENAI_API_KEY)


async def generate_telegram_post(vacancy_info: str) -> str:
    """Генерирует пост для Telegram на основе информации о вакансии"""
    
    client = Anthropic(api_key=ANTHROPIC_API_KEY)
    
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
    
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return message.content[0].text


# Для OpenAI версия функции:
"""
async def generate_telegram_post_openai(vacancy_info: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": "Ты помощник, который создаёт привлекательные посты для Telegram-канала о работе."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000
    )
    
    return response.choices[0].message.content
"""