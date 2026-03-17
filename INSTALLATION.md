# Инструкция по установке / Installation Guide

## Требования / Requirements

### Обязательные / Required
- **Python 3.10+** (3.10, 3.11, или 3.12)
- pip (менеджер пакетов Python)
- Telegram Bot Token (получить у @BotFather)

### Рекомендуемые / Recommended
- Virtual environment (venv или virtualenv)
- Git для клонирования репозитория

---

## Быстрая установка / Quick Install

### 1. Клонируйте репозиторий / Clone repository
```bash
git clone https://github.com/GenaCollection/fincredit-loan-calculator-bot.git
cd fincredit-loan-calculator-bot
```

### 2. Создайте виртуальное окружение / Create virtual environment
```bash
python3 -m venv venv

# На Linux/Mac:
source venv/bin/activate

# На Windows:
venv\Scripts\activate
```

### 3. Установите зависимости / Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Настройте переменные окружения / Configure environment
Создайте файл `.env` в корневой папке проекта:
```bash
BOT_TOKEN=your_telegram_bot_token_here
DATABASE_URL=sqlite:///fincredit.db
```

### 5. Запустите бота / Run the bot
```bash
python bot.py
```

---

## Проверка совместимости / Compatibility Check

### Проверьте версию Python / Check Python version:
```bash
python --version
# Должно быть: Python 3.10.x или выше / Should be: Python 3.10.x or higher
```

### Проверьте установленные пакеты / Check installed packages:
```bash
pip list
```

---

## Решение проблем / Troubleshooting

### Ошибка ImportError
Если получаете `ImportError`, убедитесь что:
1. Все зависимости установлены: `pip install -r requirements.txt`
2. Используете Python 3.10+: `python --version`
3. Активировано виртуальное окружение

### Ошибка с python-telegram-bot
Если бот не запускается из-за python-telegram-bot:
```bash
pip uninstall python-telegram-bot
pip install python-telegram-bot==22.7
```

### Проблемы с SQLAlchemy
```bash
pip install --upgrade SQLAlchemy==2.0.48
```

---

## Обновление / Update

```bash
git pull
pip install -r requirements.txt --upgrade
python bot.py
```

---

## Поддержка / Support

Вопросы и проблемы: [GitHub Issues](https://github.com/GenaCollection/fincredit-loan-calculator-bot/issues)
