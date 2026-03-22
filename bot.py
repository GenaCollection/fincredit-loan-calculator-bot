#!/usr/bin/env python
# -*- coding: utf-8 -*-
\"\"\"
FinCredit Loan Calculator Bot
Main entry point for the Telegram bot application.
\"\"\"
import logging
from telegram import BotCommand
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
import config
from database import init_db
from handlers.start import start_command, help_command, button_callback, handle_add_payment_message
from handlers.calculator import calculator_handler
from handlers.manage_loan import edit_loan_handler
from handlers.settings import settings_handler, change_language

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)
logging.getLogger(\"httpx\").setLevel(logging.WARNING)

async def set_commands(application):
    \"\"\"Set bot commands menu\"\"\"
    commands = [
        BotCommand(\"start\", \"Запустить бота / Start bot\"),
        BotCommand(\"help\", \"Помощь / Help\"),
    ]
    await application.bot.set_my_commands(commands)
    logger.info(\"Bot commands set\")

def main():
    \"\"\"Start the bot.\"\"\"
    if not config.BOT_TOKEN:
        raise RuntimeError(
            \"BOT_TOKEN is not set. Create a .env file (or set environment variable) with BOT_TOKEN=... \"
            \"and restart.\"
        )

    # Initialize database
    init_db()
    logger.info(\"Database initialized\")

    # Create the Application
    application = (
        Application.builder()
        .token(config.BOT_TOKEN)
        .job_queue(None)
        .post_init(set_commands)
        .build()
    )

    # Register handlers - ORDER MATTERS! Specific patterns BEFORE general handlers
    application.add_handler(CommandHandler(\"start\", start_command))
    application.add_handler(CommandHandler(\"help\", help_command))
    
    # Specific conversation handlers MUST be added BEFORE general button_callback
    application.add_handler(calculator_handler) # ConversationHandler for NEW loan
    application.add_handler(edit_loan_handler)   # ConversationHandler for EDITING loan
    
    # Settings and language
    application.add_handler(CallbackQueryHandler(settings_handler, pattern='^settings$'))
    application.add_handler(CallbackQueryHandler(change_language, pattern='^lang_'))
    
    # Text handler for \"add payment\" or other general messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_add_payment_message))
    
    # General callback handler MUST be LAST to avoid catching specific patterns
    application.add_handler(CallbackQueryHandler(button_callback))

    logger.info(\"Starting FinCredit Loan Calculator Bot...\")
    application.run_polling(allowed_updates=True)

if __name__ == '__main__':
    main()
