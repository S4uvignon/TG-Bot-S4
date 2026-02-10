import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY') # Ключ от Google AI Studio

HH_API_BASE_URL = 'https://api.hh.ru'
ADMIN_IDS = [1183964350]
