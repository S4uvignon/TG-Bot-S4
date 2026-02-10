import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY') # Ключ от Google AI Studio
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_BASE_URL = os.getenv('GROQ_BASE_URL', 'https://api.groq.com/openai/v1')

HH_API_BASE_URL = 'https://api.hh.ru'

ADMIN_IDS = [1183964350]
