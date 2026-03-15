import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Database Configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///fincredit.db')

# Default Settings
DEFAULT_LANGUAGE = 'ru'
SUPPORTED_LANGUAGES = ['ru', 'en', 'hy']

# Loan Settings
MAX_LOANS_PER_USER = 5
DEFAULT_LOAN_NAME_PREFIX = 'Кредит'

# Reminder Settings
DEFAULT_REMINDER_DAYS_BEFORE = 1
DEFAULT_REMINDER_TIME = '09:00'
DEFAULT_TIMEZONE = 'Asia/Yerevan'

# Payment Types
PAYMENT_TYPE_ANNUITY = 'annuity'
PAYMENT_TYPE_DIFFERENTIATED = 'differentiated'
