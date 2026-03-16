"""Start command handlers with localization support"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import get_session
from database.models import User
from localization import get_text  # ← ВОТ ГДЕ ИСПОЛЬЗУЕТСЯ!
import logging

logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    session = get_session()
    
    try:
        # Check if user exists in database
        db_user = session.query(User).filter_by(telegram_id=user.id).first()
        if not db_user:
            # Create new user with default language (Russian)
            db_user = User(
                telegram_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                language='ru'  # По умолчанию русский
            )
            session.add(db_user)
            session.commit()
        
        # Получаем текст приветствия НА ЯЗЫКЕ ПОЛЬЗОВАТЕЛЯ
        welcome_text = get_text(user.id, 'welcome')
        
        # Получаем тексты кнопок НА ЯЗЫКЕ ПОЛЬЗОВАТЕЛЯ
        keyboard = [
            [InlineKeyboardButton(
                get_text(user.id, 'btn_new_calc'), 
                callback_data="new_calc"
            )],
            [InlineKeyboardButton(
                get_text(user.id, 'btn_my_loans'), 
                callback_data="my_loans"
            )],
            [InlineKeyboardButton(
                get_text(user.id, 'btn_help'), 
                callback_data="help"
            ),
             InlineKeyboardButton(
                get_text(user.id, 'btn_settings'), 
                callback_data="settings"
            )]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    finally:
        session.close()


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    user = update.effective_user
    
    # Получаем текст справки НА ЯЗЫКЕ ПОЛЬЗОВАТЕЛЯ
    help_text = get_text(user.id, 'help_text')
    
    await update.message.reply_text(help_text, parse_mode='Markdown')


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    
    if query.data == "back_to_menu":
        # Показываем главное меню
        welcome_text = get_text(user.id, 'main_menu') + '\n\n' + get_text(user.id, 'welcome')
        
        keyboard = [
            [InlineKeyboardButton(
                get_text(user.id, 'btn_new_calc'), 
                callback_data="new_calc"
            )],
            [InlineKeyboardButton(
                get_text(user.id, 'btn_my_loans'), 
                callback_data="my_loans"
            )],
            [InlineKeyboardButton(
                get_text(user.id, 'btn_help'), 
                callback_data="help"
            ),
             InlineKeyboardButton(
                get_text(user.id, 'btn_settings'), 
                callback_data="settings"
            )]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            welcome_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    elif query.data == "help":
        help_text = get_text(user.id, 'help_text')
        
        await query.edit_message_text(
            help_text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    get_text(user.id, 'btn_back'), 
                    callback_data="back_to_menu"
                )
            ]])
        )
    
    elif query.data == "my_loans":
        # Временно - будет заменено на полный handler
        my_loans_text = get_text(user.id, 'my_loans_title') + get_text(user.id, 'my_loans_empty')
        
        await query.edit_message_text(
            my_loans_text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    get_text(user.id, 'btn_back'), 
                    callback_data="back_to_menu"
                )
            ]])
        )
