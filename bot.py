#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FinCredit Loan Calculator Bot
Main entry point for the Telegram bot application.
"""
import logging
import asyncio
from telegram import BotCommand
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
import config
from database import init_db
from handlers.start import start_command, help_command, button_callback
from handlers.calculator import calculator_handler, my_loans_handler
from handlers.settings import settings_handler, change_language

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def set_commands(application):
    """Set bot commands menu"""
    commands = [
        BotCommand("start", "Запустить бота / Start bot"),
        BotCommand("help", "Помощь / Help"),
    ]
    await application.bot.set_my_commands(commands)
    logger.info("Bot commands set")


async def main():
    """Start the bot."""
    # Initialize database
    init_db()
    logger.info("Database initialized")
    
    # Create the Application
    application = Application.builder().token(config.BOT_TOKEN).job_queue(None).post_init(set_commands).build()
    
    # Register handlers - ORDER MATTERS! Specific patterns BEFORE general handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(calculator_handler)  # ConversationHandler
    application.add_handler(my_loans_handler)  # ConversationHandler for my loans
    
    # Specific callback handlers MUST be registered BEFORE general button_callback
    application.add_handler(CallbackQueryHandler(settings_handler, pattern='^settings$'))  # Settings
    application.add_handler(CallbackQueryHandler(change_language, pattern='^lang_'))  # Language change
    
    # General callback handler MUST be LAST to avoid catching specific patterns
    application.add_handler(CallbackQueryHandler(button_callback))
    
    logger.info("Starting FinCredit Loan Calculator Bot...")
    await application.run_polling(allowed_updates=True)


if __name__ == '__main__':
    asyncio.run(main())
