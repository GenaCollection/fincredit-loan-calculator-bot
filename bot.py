#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
FinCredit Loan Calculator Bot
Main entry point for the Telegram bot application.
"""

import logging

from telegram import BotCommand, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

import config
from database.database import init_db

from handlers.start import (
    start_command,
    help_command,
    route_text_messages,
    myloans_command,
)
from handlers.calculator import calculator_handler
from handlers.calculator import calculator_handler, _entry_new_calc_reply
from handlers.manage_loan import edit_loan_handler
from handlers.settings import settings_handler, change_language, settings_command
from handlers.loan_schedule import loan_schedule_callback
from handlers.add_payment import add_payment_handler

from callbacks import parse_callback_data, CallbackType

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)


async def set_commands(application: Application):
    """Set bot commands menu"""
    commands = [
        BotCommand("start", "Главное меню / Main Menu"),
        BotCommand("myloans", "Мои кредиты / My Loans"),
        BotCommand("help", "Помощь / Help"),
        BotCommand("settings", "Настройки / Settings"),
    ]
    await application.bot.set_my_commands(commands)
    logger.info("Bot commands set")


async def main_menu_callback_router(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Общий роутер для callback-ов главного меню, помощи и настроек."""
    query = update.callback_query
    data = query.data

    try:
        cb_type, parts = parse_callback_data(data)
    except Exception as e:
        logger.warning("Failed to parse callback data '%s': %s", data, e)
        return

    if cb_type is CallbackType.MAIN_MENU:
        action = parts[0] if parts else "open"

        if action == "new_calc":
            from handlers.calculator import _entry_new_calc_reply

            await _entry_new_calc_reply(update, context)
        elif action == "my_loans":
            await myloans_command(update, context)
        else:
            await start_command(update, context)

    elif cb_type is CallbackType.HELP:
        await help_command(update, context)

    elif cb_type is CallbackType.SETTINGS:
        await settings_command(update, context)

    else:
        logger.info("Unhandled callback type in main_menu_callback_router: %s", cb_type)


def main():
    """Start the bot."""
    if not config.BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN is not set. Create a .env file (or set environment variable) "
            "with BOT_TOKEN=... and restart."
        )

    # Initialize database
    init_db()
    logger.info("Database initialized")

    # Create the Application
    application = (
        Application.builder()
        .token(config.BOT_TOKEN)
        .post_init(set_commands)
        .build()
    )

    # === Command handlers ===
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("myloans", myloans_command))
    application.add_handler(CommandHandler("settings", settings_command))

    # === Conversation / complex handlers ===
    # Они регистрируются до общих callback-обработчиков
    application.add_handler(calculator_handler)
    application.add_handler(edit_loan_handler)
    application.add_handler(add_payment_handler)

    # График платежей — использует старый формат callback_data "loan_schedule_..."
    application.add_handler(
        CallbackQueryHandler(
            loan_schedule_callback,
            pattern=r"^loan_schedule_\d+_\d+$",
        )
    )

    # === Новый роутер для callback-ов главного меню/хелпа/настроек ===
    application.add_handler(
        CallbackQueryHandler(
            main_menu_callback_router,
            pattern=r"^(main_menu|help|settings):",
        )
    )

    # === Text messages (reply keyboard) ===
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, route_text_messages)
    )

    logger.info("Starting FinCredit Loan Calculator Bot...")
    application.run_polling(allowed_updates=True)


if __name__ == "__main__":
    main()
