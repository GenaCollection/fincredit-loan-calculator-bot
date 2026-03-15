#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FinCredit Loan Calculator Bot
Main entry point for the Telegram bot application.
"""

import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
import config
from database import init_db  # ← ИСПРАВЛЕНО! Было "from handlers import init_db"
from handlers.start import start_command, help_command, button_callback

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
    
    # Create the Application
    application = Application.builder().token(config.BOT_TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button_callback))

    # Start the bot
    logger.info("Starting FinCredit Loan Calculator Bot...")
    application.run_polling(allowed_updates=True)


if __name__ == '__main__':
    main()
