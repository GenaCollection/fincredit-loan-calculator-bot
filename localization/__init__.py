"""Localization package"""

from localization import ru, en, hy

LANGUAGES = {
    'ru': ru.TEXTS,
    'en': en.TEXTS,
    'hy': hy.TEXTS
}

def get_text(key, lang='ru'):
    """Get localized text"""
    return LANGUAGES.get(lang, LANGUAGES['ru']).get(key, key)
