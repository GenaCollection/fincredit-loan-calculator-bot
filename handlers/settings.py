"""Settings handler for language selection"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import get_session
from database.models import User
from localization import get_text, get_language_name
import logging

logger = logging.getLogger(__name__)


async def settings_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show settings menu"""
    query = update.callback_query
    await query.answer()

    user = query.from_user
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

        current_lang = db_user.language

        text = get_text(user.id, 'settings_title')
        text += f"\n\n{get_text(user.id, 'settings_language', lang=get_language_name(current_lang))}"

        keyboard = [
            [
                InlineKeyboardButton(get_text(user.id, 'btn_lang_ru'), callback_data="lang_ru"),
                InlineKeyboardButton(get_text(user.id, 'btn_lang_en'), callback_data="lang_en")
            ],
            [InlineKeyboardButton(get_text(user.id, 'btn_lang_hy'), callback_data="lang_hy")],
            [InlineKeyboardButton(get_text(user.id, 'btn_back'), callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"Error in settings: {e}")
        error_text = get_text(user.id, 'error_generic')
        await query.edit_message_text(error_text)
    finally:
        session.close()


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

            success_text = get_text(user.id, 'language_changed')
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
