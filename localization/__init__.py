"""Localization helper - Помощник для работы с языками"""
from . import ru, en, hy
from database import get_session
from database.models import User

# Карта языковых модулей
LANGUAGES = {
    'ru': ru.TEXTS,
    'en': en.TEXTS,
    'hy': hy.TEXTS
}

# Названия языков
LANGUAGE_NAMES = {
    'ru': 'Русский 🇷🇺',
    'en': 'English 🇬🇧',
    'hy': 'Հայերեն 🇦🇲'
}

# Язык по умолчанию
DEFAULT_LANGUAGE = 'ru'


def get_text(user_id: int, key: str, **kwargs) -> str:
    """
    Получить текст на языке пользователя
    
    Args:
        user_id: Telegram ID пользователя
        key: Ключ текста из словаря TEXTS
        **kwargs: Параметры для форматирования строки
    
    Returns:
        Отформатированный текст на языке пользователя
    
    Example:
        text = get_text(user_id, 'calc_amount_set', amount=1000000)
    """
    session = get_session()
    try:
        # Получаем язык пользователя
        user = session.query(User).filter_by(telegram_id=user_id).first()
        lang = user.language if user else DEFAULT_LANGUAGE
        
        # Проверяем существование языка
        if lang not in LANGUAGES:
            lang = DEFAULT_LANGUAGE
        
        # Получаем текст
        texts = LANGUAGES[lang]
        text = texts.get(key, f'[Missing: {key}]')
        
        # Форматируем с параметрами
        if kwargs:
            try:
                text = text.format(**kwargs)
            except (KeyError, ValueError) as e:
                # Если ошибка форматирования, возвращаем исходный текст
                pass
        
        return text
    finally:
        session.close()


def get_user_language(user_id: int) -> str:
    """
    Получить язык пользователя
    
    Args:
        user_id: Telegram ID пользователя
    
    Returns:
        Код языка ('ru', 'en', 'hy')
    """
    session = get_session()
    try:
        user = session.query(User).filter_by(telegram_id=user_id).first()
        return user.language if user else DEFAULT_LANGUAGE
    finally:
        session.close()


def set_user_language(user_id: int, language: str) -> bool:
    """
    Установить язык пользователя
    
    Args:
        user_id: Telegram ID пользователя
        language: Код языка ('ru', 'en', 'hy')
    
    Returns:
        True если успешно, False если ошибка
    """
    if language not in LANGUAGES:
        return False
    
    session = get_session()
    try:
        user = session.query(User).filter_by(telegram_id=user_id).first()
        if user:
            user.language = language
            session.commit()
            return True
        return False
    except Exception:
        session.rollback()
        return False
    finally:
        session.close()


def get_language_name(lang_code: str) -> str:
    """
    Получить название языка
    
    Args:
        lang_code: Код языка
    
    Returns:
        Название языка с флагом
    """
    return LANGUAGE_NAMES.get(lang_code, lang_code)


# Экспортируем функции
__all__ = [
    'get_text',
    'get_user_language', 
    'set_user_language',
    'get_language_name',
    'LANGUAGES',
    'LANGUAGE_NAMES',
    'DEFAULT_LANGUAGE'
]
