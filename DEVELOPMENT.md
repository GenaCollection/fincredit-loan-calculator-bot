# Development Guide / Руководство по разработке

## Текущий статус проекта

### ✅ Что уже реализовано:

1. **Базовая структура проекта**
   - `config.py` - конфигурация с поддержкой 3 языков
   - `bot.py` - точка входа приложения
   - `requirements.txt` - все зависимости

2. **database/** - Работа с базой данных
   - `models.py` - модели User, Loan, Payment, ExtraPayment ✅
   - `__init__.py` - инициализация пакета ✅
   - `database.py` - подключение к БД ⏳ НУЖНО СОЗДАТЬ

3. **utils/** - Утилиты
   - `calculations.py` - формулы расчёта кредита ✅
   - `__init__.py` ⏳ НУЖНО СОЗДАТЬ
   - `keyboards.py` - клавиатуры меню ⏳ НУЖНО СОЗДАТЬ

4. **localization/** - Локализация ⏳ НУЖНО СОЗДАТЬ
   - `ru.py` - русский язык
   - `en.py` - английский язык
   - `hy.py` - армянский язык

5. **handlers/** - Обработчики команд ⏳ НУЖНО СОЗДАТЬ
   - `start.py` - команда /start
   - `calculator.py` - создание расчёта
   - `my_loans.py` - управление кредитами
   - `settings.py` - настройки

---

## 🚀 Что нужно доделать

### 1. Создать database/database.py

```python
"""Database connection and session management"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import config
from database.models import Base

engine = None
Session = None

def init_db():
    """Initialize database and create all tables"""
    global engine, Session
    
    engine = create_engine(config.DATABASE_URL, echo=False)
    Session = scoped_session(sessionmaker(bind=engine))
    
    # Create all tables
    Base.metadata.create_all(engine)
    
def get_session():
    """Get database session"""
    if Session is None:
        init_db()
    return Session()
```

### 2. Создать utils/__init__.py

```python
"""Utils package initialization"""

from utils.calculations import (
    calculate_annuity_payment,
    calculate_annuity_schedule,
    calculate_differentiated_schedule,
    calculate_loan_totals
)

__all__ = [
    'calculate_annuity_payment',
    'calculate_annuity_schedule',
    'calculate_differentiated_schedule',
    'calculate_loan_totals',
]
```

### 3. Создать localization/ru.py

```python
"""Russian localization"""

TEXTS = {
    # Welcome
    'welcome': 'Добро пожаловать в FinCredit! 💰\\n\\nЯ помогу вам рассчитать кредит и управлять платежами.',
    
    # Main menu
    'main_menu': 'Главное меню',
    'btn_new_calc': '💳 Новый расчёт',
    'btn_my_loans': '📊 Мои кредиты',
    'btn_help': '❓ Помощь',
    'btn_settings': '⚙️ Настройки',
    'btn_back': '◀️ Назад',
    
    # Calculation
    'calc_amount': 'Введите сумму кредита (например: 1000000):',
    'calc_rate': 'Введите процентную ставку (например: 12.5):',
    'calc_term': 'Введите срок кредита в месяцах (например: 24):',
    'calc_payment_type': 'Выберите тип платежа:',
    'btn_annuity': 'Аннуитетный',
    'btn_differentiated': 'Дифференцированный',
    
    # Results
    'results_title': '📊 Результаты расчёта',
    'monthly_payment': 'Ежемесячный платёж',
    'total_payment': 'Общая сумма выплат',
    'overpayment': 'Переплата',
    'btn_save_loan': '💾 Сохранить кредит',
    'btn_new_calc_2': '🔄 Новый расчёт',
}
```

### 4. Создать utils/keyboards.py

```python
"""Keyboard layouts for bot menus"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_main_menu(lang='ru'):
    """Get main menu keyboard"""
    keyboard = [
        [InlineKeyboardButton("💳 Новый расчёт", callback_data="new_calc")],
        [InlineKeyboardButton("📊 Мои кредиты", callback_data="my_loans")],
        [InlineKeyboardButton("❓ Помощь", callback_data="help"),
         InlineKeyboardButton("⚙️ Настройки", callback_data="settings")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_payment_type_keyboard():
    """Get payment type selection keyboard"""
    keyboard = [
        [InlineKeyboardButton("Аннуитетный", callback_data="type_annuity")],
        [InlineKeyboardButton("Дифференцированный", callback_data="type_diff")],
        [InlineKeyboardButton("◀️ Назад", callback_data="back")]
    ]
    return InlineKeyboardMarkup(keyboard)
```

### 5. Создать handlers/start.py

```python
"""Start command handler"""

from telegram import Update
from telegram.ext import ContextTypes
from database import get_session, User
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
```

### 6. Обновить bot.py

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
import config
from database import init_db
from handlers.start import start_command

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Start the bot."""
    # Initialize database
    init_db()
    logger.info("Database initialized")
    
    # Create application
    application = Application.builder().token(config.BOT_TOKEN).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start_command))
    # TODO: Add more handlers
    
    # Start the bot
    logger.info("Starting FinCredit Loan Calculator Bot...")
    application.run_polling(allowed_updates=True)

if __name__ == '__main__':
    main()
```

---

## 📝 Пошаговая инструкция по доработке

### Шаг 1: Создайте недостающие файлы
Используйте примеры кода выше для создания файлов:
- `database/database.py`
- `utils/__init__.py`
- `utils/keyboards.py`
- `localization/ru.py`
- `handlers/__init__.py`
- `handlers/start.py`

### Шаг 2: Обновите bot.py
Добавьте импорты и регистрацию обработчиков согласно примеру выше.

### Шаг 3: Добавьте английскую и армянскую локализацию
Создайте `localization/en.py` и `localization/hy.py` по аналогии с `ru.py`.

### Шаг 4: Реализуйте обработчики
Создайте файлы в папке `handlers/` для каждой функции бота.

### Шаг 5: Тестирование
```bash
python bot.py
```

---

## 🔧 Полезные ссылки

- [python-telegram-bot Documentation](https://docs.python-telegram-bot.org/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Telegram Bot API](https://core.telegram.org/bots/api)

---

## 💡 Советы

1. Используйте виртуальное окружение
2. Тестируйте каждую функцию отдельно
3. Добавляйте логирование для отладки
4. Храните токен бота в безопасности (.env файл)
5. Делайте коммиты после каждого рабочего изменения

---

**Удачи в разработке! 🚀**
