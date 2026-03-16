"""Start command handlers"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import get_session
from database.models import User
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
            # Create new user
            db_user = User(
                telegram_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                language='ru'
            )
            session.add(db_user)
            session.commit()
        
        welcome_text = (
            "Добро пожаловать в FinCredit! 💰\n\n"
            "Я помогу вам:\n"
            "✅ Рассчитать ежемесячный платёж по кредиту\n"
            "✅ Учесть досрочные платежи и страховку\n"
            "✅ Сравнить разные стратегии погашения\n"
            "✅ Сохранить и отслеживать кредиты\n\n"
            "Выберите действие:"
        )
        
        keyboard = [
            [InlineKeyboardButton("💳 Новый расчёт", callback_data="new_calc")],
            [InlineKeyboardButton("📊 Мои кредиты", callback_data="my_loans")],
            [InlineKeyboardButton("❓ Помощь", callback_data="help"),
             InlineKeyboardButton("⚙️ Настройки", callback_data="settings")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_text,
            reply_markup=reply_markup
        )
    finally:
        session.close()


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = (
        "📖 *Помощь*\n\n"
        "*Команды:*\n"
        "/start - Главное меню\n"
        "/help - Эта справка\n\n"
        "*Функции:*\n"
        "💳 Новый расчёт - Рассчитать кредит\n"
        "📊 Мои кредиты - Список ваших кредитов\n"
        "⚙️ Настройки - Язык и уведомления"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "back_to_menu":
        await start_command(update, context)
    elif query.data == "help":
        await query.edit_message_text(
            "📖 *Помощь*\n\n"
            "Используйте кнопки меню для навигации.",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("◀️ Назад", callback_data="back_to_menu")
            ]])
        )
    elif query.data == "my_loans":
        await query.edit_message_text(
            "📊 *Мои кредиты*\n\n"
            "У вас пока нет сохранённых кредитов.",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("◀️ Назад", callback_data="back_to_menu")
            ]])
        )
