import httpx
import re
import time
from typing import Optional, Dict


# Кэш токена: { "access_token": str, "expires_at": float }
_token_cache: Dict = {}


def extract_vacancy_id(url: str) -> Optional[str]:
    """Извлекает ID вакансии из URL hh.ru"""
    patterns = [
        r'vacancy/(\d+)',
        r'vacancies/(\d+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


async def _get_access_token(client_id: str, client_secret: str) -> Optional[str]:
    """
    Получает access_token через Client Credentials OAuth flow.
    Кэширует токен до истечения срока действия.
    """
    now = time.time()

    # Возвращаем кэшированный токен, если он ещё действителен (с запасом 60 сек)
    if _token_cache.get("access_token") and _token_cache.get("expires_at", 0) > now + 60:
        return _token_cache["access_token"]

    url = "https://hh.ru/oauth/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "TG-Vacancy-Bot/1.0",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, data=data, headers=headers, timeout=15.0)
            response.raise_for_status()
            token_data = response.json()

            access_token = token_data.get("access_token")
            expires_in = token_data.get("expires_in", 86400)  # по умолчанию 24 часа

            _token_cache["access_token"] = access_token
            _token_cache["expires_at"] = now + expires_in

            print(f"HH OAuth: получен новый токен, действует {expires_in} сек.")
            return access_token

        except httpx.HTTPStatusError as e:
            print(f"Ошибка получения токена HH: {e.response.status_code} — {e.response.text}")
            return None
        except httpx.HTTPError as e:
            print(f"Сетевая ошибка при получении токена HH: {e}")
            return None


async def get_vacancy_info(vacancy_id: str, client_id: str, client_secret: str) -> Optional[Dict]:
    """Получает информацию о вакансии через API HH с OAuth авторизацией"""

    access_token = await _get_access_token(client_id, client_secret)
    if not access_token:
        print("Не удалось получить access_token, запрос отменён.")
        return None

    url = f"https://api.hh.ru/vacancies/{vacancy_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "TG-Vacancy-Bot/1.0",
        "Accept": "application/json",
        "HH-User-Agent": "TG-Vacancy-Bot/1.0",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            print(f"HH API статус: {response.status_code}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP ошибка от HH API: {e.response.status_code} — {e.response.text}")
            return None
        except httpx.HTTPError as e:
            print(f"Ошибка при запросе к HH API: {e}")
            return None


def format_vacancy_data(vacancy: Dict) -> str:
    """Форматирует данные вакансии для передачи в AI"""
    
    # Зарплата
    salary = "Не указана"
    if vacancy.get('salary'):
        sal = vacancy['salary']
        if sal['from'] and sal['to']:
            salary = f"{sal['from']:,} - {sal['to']:,} {sal['currency']}"
        elif sal['from']:
            salary = f"от {sal['from']:,} {sal['currency']}"
        elif sal['to']:
            salary = f"до {sal['to']:,} {sal['currency']}"
    
    # Опыт
    experience = vacancy.get('experience', {}).get('name', 'Не указан')
    
    # Занятость и график
    employment = vacancy.get('employment', {}).get('name', 'Не указана')
    schedule = vacancy.get('schedule', {}).get('name', 'Не указан')
    
    # Навыки
    skills = [skill['name'] for skill in vacancy.get('key_skills', [])]
    skills_str = ', '.join(skills) if skills else 'Не указаны'
    
    formatted = f"""
Название: {vacancy['name']}
Компания: {vacancy['employer']['name']}
Город: {vacancy['area']['name']}
Зарплата: {salary}
Опыт: {experience}
Занятость: {employment}
График: {schedule}
Ключевые навыки: {skills_str}

Описание вакансии:
{vacancy.get('description', 'Описание отсутствует')}
"""
    
    return formatted.strip()
