import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
# OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

HH_API_BASE_URL = 'https://api.hh.ru'