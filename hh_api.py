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


def extract_vacancy_url(text: str) -> Optional[str]:
    """Извлекает полную ссылку на вакансию из текста"""
    # Ищем ссылку на hh.ru
    patterns = [
        r'https?://[^\s]*hh\.ru/vacancy/\d+[^\s]*',
        r'https?://[^\s]*hh\.ru/vacancies/\d+[^\s]*',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            # Убираем лишние параметры и якоря
            url = match.group(0)
            # Очищаем от возможных символов в конце
            url = re.sub(r'[.,;!?)\]]+$', '', url)
            return url
    return None


async def get_vacancy_info(vacancy_id: str) -> Optional[Dict]:
    """Получает информацию о вакансии через API HH"""
    url = f'https://api.hh.ru/vacancies/{vacancy_id}'
    
    async with httpx.AsyncClient(verify=False) as client:
        try:
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            print(f"Ошибка при запросе к HH API: {e}")
            return None


def format_vacancy_data(vacancy: Dict, vacancy_url: Optional[str] = None) -> str:
    """Форматирует данные вакансии для передачи в AI"""
    
    try:
        # Зарплата
        salary = "Не указана"
        if vacancy.get('salary'):
            sal = vacancy['salary']
            if sal.get('from') and sal.get('to'):
                salary = f"{sal['from']:,} - {sal['to']:,} {sal['currency']}"
            elif sal.get('from'):
                salary = f"от {sal['from']:,} {sal['currency']}"
            elif sal.get('to'):
                salary = f"до {sal['to']:,} {sal['currency']}"
        
        # Опыт
        experience = vacancy.get('experience', {}).get('name', 'Не указан')
        
        # Занятость и график
        employment = vacancy.get('employment', {}).get('name', 'Не указана')
        schedule = vacancy.get('schedule', {}).get('name', 'Не указан')
        
        # Навыки
        skills = [skill.get('name', '') for skill in vacancy.get('key_skills', [])]
        skills_str = ', '.join(skills) if skills else 'Не указаны'
        
        # Формируем ссылку - просто используем ID
        vacancy_id = vacancy.get('id', '')
        link = vacancy_url if vacancy_url else f"https://hh.ru/vacancy/{vacancy_id}"
        
        formatted = f"""
Название: {vacancy.get('name', 'Не указано')}
Компания: {vacancy.get('employer', {}).get('name', 'Не указана')}
Город: {vacancy.get('area', {}).get('name', 'Не указан')}
Зарплата: {salary}
Опыт: {experience}
Занятость: {employment}
График: {schedule}
Ключевые навыки: {skills_str}
Ссылка на вакансию: {link}

Описание вакансии:
{vacancy.get('description', 'Описание отсутствует')}
"""
        
        return formatted.strip()
        
    except Exception as e:
        print(f"ERROR в format_vacancy_data: {e}")
        import traceback
        traceback.print_exc()
        raise
