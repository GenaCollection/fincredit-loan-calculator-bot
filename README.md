# FinCredit Loan Calculator Bot 💰

A feature-rich Telegram bot for loan calculations with multi-language support (Russian, English, Armenian). Calculate monthly payments, track multiple loans, and receive payment reminders.

## Features ✨

- **Loan Calculations**: Calculate monthly payments for annuity and differentiated payment types
- **Multi-Language Support**: Interface available in Russian, English, and Armenian
- **Loan Management**: Track up to 5 loans simultaneously
- **Payment Reminders**: Get automated reminders before payment due dates
- **Extra Payments**: Add one-time or recurring extra payments to reduce loan duration
- **Payment Schedule**: View detailed payment schedules with dates
- **User-Friendly Interface**: Step-by-step wizard for easy loan creation

## Technologies 🛠️

- Python 3.9+
- python-telegram-bot 20.7
- SQLAlchemy 2.0
- APScheduler 3.10
- SQLite/PostgreSQL

## Installation 📦

### Prerequisites

- Python 3.9 or higher
- Telegram Bot Token (get it from [@BotFather](https://t.me/BotFather))

### Setup

1. Clone the repository:
```bash
git clone https://github.com/GenaCollection/fincredit-loan-calculator-bot.git
cd fincredit-loan-calculator-bot
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
```

Edit `.env` file and add your bot token:
```
BOT_TOKEN=your_bot_token_here
```

5. Run the bot:
```bash
python bot.py
```

## Usage 🚀

### Bot Commands

- `/start` - Start the bot and see the main menu
- `/help` - Get help and usage instructions
- `/settings` - Change language and reminder settings

### Main Menu Options

- **Новый расчёт** (New Calculation) - Create a new loan calculation
- **Мои кредиты** (My Loans) - View and manage your existing loans
- **Помощь** (Help) - Get detailed help information
- **Настройки** (Settings) - Configure language and reminders

### Creating a Loan

1. Click "Новый расчёт"
2. Enter loan amount
3. Enter interest rate (%)
4. Enter loan term (months)
5. Select payment type (Annuity/Differentiated)
6. Optionally add start date
7. View results and save the loan

## Configuration ⚙️

### Environment Variables

- `BOT_TOKEN` - Your Telegram bot token (required)
- `DATABASE_URL` - Database connection string (default: sqlite:///fincredit.db)

### Default Settings

- Maximum loans per user: 5
- Default reminder: 1 day before payment at 9:00 AM (Yerevan timezone)
- Supported languages: Russian, English, Armenian

## Project Structure 📁

```
fincredit-loan-calculator-bot/
│
├── bot.py                 # Main entry point
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📄

This project is open source and available under the MIT License.

## Support 💬

If you have any questions or issues, please open an issue on GitHub.

## Roadmap 🗺️

- [ ] Add database models and migrations
- [ ] Implement bot handlers and commands
- [ ] Add localization files for RU/EN/HY
- [ ] Implement loan calculation logic
- [ ] Add reminder scheduler
- [ ] Add payment tracking features
- [ ] Deploy to production

---

Made with ❤️ for better loan management
