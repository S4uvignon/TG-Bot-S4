import httpx
import re
from typing import Optional, Dict


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


async def get_vacancy_info(vacancy_id: str) -> Optional[Dict]:
    """Получает информацию о вакансии через API HH"""
    url = f'https://api.hh.ru/vacancies/{vacancy_id}'
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
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