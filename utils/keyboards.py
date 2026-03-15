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