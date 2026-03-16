#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FinCredit Loan Calculator Bot
Main entry point for the Telegram bot application.
"""
import logging
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import config
from database import init_db
from handlers.start import start_command, help_command, button_callback
from handlers.calculator import calculator_handler

# Enable logging
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
    
    # Create the Updater and pass it your bot's token
    # ИСПРАВЛЕНО: убран use_context=True (в версии 13.15 он по умолчанию True)
    updater = Updater(config.BOT_TOKEN)
    
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    
    # Register handlers
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(calculator_handler)  # НОВЫЙ HANDLER
    dispatcher.add_handler(CallbackQueryHandler(button_callback))
    
    # Start the bot
    logger.info("Starting FinCredit Loan Calculator Bot...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
