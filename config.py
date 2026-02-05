import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
# DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
# ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
# OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

HH_API_BASE_URL = 'https://api.hh.ru'
GROQ_BASE_URL = 'https://api.groq.com/openai/v1'
# DEEPSEEK_BASE_URL = 'https://api.deepseek.com'

ADMIN_IDS = [1183964350]
