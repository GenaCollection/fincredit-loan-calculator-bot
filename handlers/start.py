"""Start command handler"""

from telegram import Update
from telegram.ext import ContextTypes
from database.database import get_session
from database.models import User
from utils.keyboards import get_main_menu

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    session = get_session()
    
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
        "Добро пожаловать в FinCredit! 💰\\n\\n"
        "Я помогу вам:\\n"
        "✅ Рассчитать ежемесячный платёж по кредиту\\n"
        "✅ Сохранить и отслеживать кредиты\\n"
        "✅ Получать напоминания о платежах\\n\\n"
        "Выберите действие:"
    )
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=get_main_menu()
    )
    
    session.close()


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = (
        "ℹ️ Помощь по боту FinCredit\n\n"
        "📝 Доступные команды:\n"
        "/start - Главное меню\n"
        "/help - Показать эту справку\n\n"
        "💡 Как пользоваться:\n"
        "1️⃣ Нажмите 'Новый расчёт' для создания кредита\n"
        "2️⃣ Введите параметры кредита\n"
        "3️⃣ Выберите тип платежа\n"
        "4️⃣ Сохраните результат\n\n"
        "📊 В разделе 'Мои кредиты' вы можете:\n"
        "• Просматривать сохранённые кредиты\n"
        "• Редактировать параметры\n"
        "• Добавлять внеочередные платежи\n"
        "• Настроить напоминания\n"
    )
    
    await update.message.reply_text(help_text)


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks from inline keyboard"""
    query = update.callback_query
    await query.answer()
    
    # TODO: Implement button handling logic
    await query.edit_message_text(text=f"Вы выбрали: {query.data}\n\nЭта функция скоро будет доступна!")

