"""Localization helper - Помощник для работы с языками"""

from . import ru, en, hy
from database.database import get_session
from database.models import User

# Карта языковых модулей
LANGUAGES = {
    "ru": ru.TEXTS,
    "en": en.TEXTS,
    "hy": hy.TEXTS,
}

# Названия языков
LANGUAGE_NAMES = {
    "ru": "Русский 🇷🇺",
    "en": "English 🇬🇧",
    "hy": "Հայերեն 🇦🇲",
}

# Язык по умолчанию
DEFAULT_LANGUAGE = "ru"


def get_text(user_id_or_lang, key: str, **kwargs) -> str:
    """
    Универсальное получение текста.
    Принимает либо telegram_id (int), либо код языка (str).
    """
    lang = DEFAULT_LANGUAGE

    if isinstance(user_id_or_lang, str):
        lang = user_id_or_lang
    elif isinstance(user_id_or_lang, int):
        session = get_session()
        try:
            user = (
                session.query(User)
                .filter_by(telegram_id=user_id_or_lang)
                .first()
            )
            if user:
                lang = user.language
        except Exception:
            lang = DEFAULT_LANGUAGE
        finally:
            session.close()

    if lang not in LANGUAGES:
        lang = DEFAULT_LANGUAGE

    texts = LANGUAGES[lang]
    text = texts.get(key, f"[Missing: {key}]")

    if kwargs:
        try:
            text = text.format(**kwargs)
        except (KeyError, ValueError, IndexError):
            pass

    return text


def get_user_language(user_id: int) -> str:
    """Получить язык пользователя по его telegram_id."""
    session = get_session()
    try:
        user = session.query(User).filter_by(telegram_id=user_id).first()
        return user.language if user else DEFAULT_LANGUAGE
    except Exception:
        return DEFAULT_LANGUAGE
    finally:
        session.close()


def set_user_language(user_id: int, language: str) -> bool:
    """Установить язык пользователя."""
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
    """Получить читаемое название языка по коду."""
    return LANGUAGE_NAMES.get(lang_code, lang_code)


__all__ = [
    "get_text",
    "get_user_language",
    "set_user_language",
    "get_language_name",
    "LANGUAGES",
    "LANGUAGE_NAMES",
    "DEFAULT_LANGUAGE",
]
