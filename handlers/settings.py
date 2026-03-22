"""Settings handler for language selection"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import get_session
from database.models import User
from localization import get_text, get_language_name
import logging

logger = logging.getLogger(__name__)


def _ensure_user_row(user) -> User:
    session = get_session()
    try:
        db_user = session.query(User).filter_by(telegram_id=user.id).first()
        if not db_user:
            db_user = User(
                telegram_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                language='ru'
            )
            session.add(db_user)
            session.commit()
        return db_user
    finally:
        session.close()


def build_settings_markup(user_id: int):
    session = get_session()
    try:
        db_user = session.query(User).filter_by(telegram_id=user_id).first()
        current_lang = db_user.language if db_user else 'ru'
    finally:
        session.close()

    text = get_text(user_id, 'settings_title')
    text += f"\n\n{get_text(user_id, 'settings_language', lang=get_language_name(current_lang))}"

    keyboard = [
        [
            InlineKeyboardButton(get_text(user_id, 'btn_lang_ru'), callback_data="lang_ru"),
            InlineKeyboardButton(get_text(user_id, 'btn_lang_en'), callback_data="lang_en")
        ],
        [InlineKeyboardButton(get_text(user_id, 'btn_lang_hy'), callback_data="lang_hy")],
        [InlineKeyboardButton(get_text(user_id, 'btn_back'), callback_data="main_menu")]
    ]
    return text, InlineKeyboardMarkup(keyboard)


async def settings_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show settings menu"""
    query = update.callback_query
    await query.answer()

    user = query.from_user
    try:
        _ensure_user_row(user)
        text, reply_markup = build_settings_markup(user.id)
        await query.edit_message_text(
            text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"Error in settings: {e}")
        error_text = get_text(user.id, 'error_generic')
        await query.edit_message_text(error_text)


async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show settings from /settings or when message has no callback_query."""
    user = update.effective_user
    _ensure_user_row(user)
    text, reply_markup = build_settings_markup(user.id)
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')


async def change_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Change user language"""
    query = update.callback_query
    await query.answer()

    user = query.from_user
    lang = query.data.replace('lang_', '')

    session = get_session()
    try:
        db_user = session.query(User).filter_by(telegram_id=user.id).first()
        if db_user:
            db_user.language = lang
            session.commit()

            success_text = get_text(user.id, 'language_changed', lang=get_language_name(lang))
            keyboard = [[InlineKeyboardButton(get_text(user.id, 'btn_back'), callback_data="settings")]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.edit_message_text(
                success_text,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
    except Exception as e:
        logger.error(f"Error changing language: {e}")
        error_text = get_text(user.id, 'error_generic')
        await query.edit_message_text(error_text)
    finally:
        session.close()
