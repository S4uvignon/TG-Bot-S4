from openai import OpenAI
import requests
import os
from config import GROQ_API_KEY, GROQ_BASE_URL
from prompts import get_prompt

GROQ_BASE_URL = "https://api.groq.com/openai/v1"
HF_TOKEN = os.getenv("HF_TOKEN")

async def generate_telegram_post(vacancy_info: str) -> str:
    """Генерирует пост для Telegram на основе информации о вакансии"""
    
    client = OpenAI(
        api_key=GROQ_API_KEY,
        base_url=GROQ_BASE_URL
    )
    
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


def generate_image(job_title: str) -> bytes:
    """Генерирует картинку для вакансии через HuggingFace FLUX.1-schnell"""
    
    prompt = f"Professional illustration for job vacancy: {job_title}, modern office, clean design, no text, no letters"
    
    response = requests.post(
        "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell",
        headers={"Authorization": f"Bearer {HF_TOKEN}"},
        json={"inputs": prompt},
        timeout=60
    )
    
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"HF API error: {response.status_code} {response.text}")
