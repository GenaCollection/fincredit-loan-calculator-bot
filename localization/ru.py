"""Russian localization"""

TEXTS = {
    # Welcome & Menu
    "welcome": """🎉 Добро пожаловать в *FinCredit*!

💰 Я помогу вам:
✅ Рассчитать кредит с досрочными платежами
✅ Учесть страховку и комиссии
✅ Сравнить стратегии погашения
✅ Сохранить и отслеживать кредиты
✅ Получать напоминания о платежах

Выберите действие:""",
    "main_menu": "📋 *Главное меню*",

    # Buttons
    "btn_new_calc": "💳 Новый расчёт",
    "btn_my_loans": "📊 Мои кредиты",
    "btn_help": "❓ Помощь",
    "btn_settings": "⚙️ Настройки",
    "btn_back": "◀️ Назад",
    "btn_cancel": "❌ Отменить",
    "btn_save": "💾 Сохранить",
    "btn_delete": "🗑 Удалить",
    "btn_edit": "✏️ Изменить",
    "btn_view_schedule": "📅 График платежей",
    "btn_add_extra": "💸 Досрочный платёж",

    # Calculator
    "calc_start": """💳 *Кредитный калькулятор*

Давайте рассчитаем ваш кредит!

📝 Введите *сумму кредита* (например: 1000000):""",
    "calc_amount_set": "✅ Сумма: {amount:,.0f} ₽",
    "calc_rate_set": "✅ Ставка: {rate}%",
    "calc_term_set": "✅ Срок: {months} мес.",
    "calc_payment_type": "💳 Выберите тип платежа:",
    "btn_annuity": "📊 Аннуитетный",
    "btn_differentiated": "📉 Дифференцированный",
    "annuity_info": "_Равные платежи каждый месяц_",
    "diff_info": "_Платежи уменьшаются со временем_",

    "calc_insurance": """💼 *Страховка*

Будете ли вы платить ежемесячную страховку по кредиту?""",
    "btn_insurance_yes": "✅ Да, учитывать",
    "btn_insurance_no": "❌ Нет",
    "calc_insurance_amount": "💼 Введите *сумму ежемесячной страховки* (например: 1500):",

    "calc_extra_payments": """💸 *Досрочное погашение*

Планируете ли вы делать досрочные платежи?""",
    "btn_extra_yes": "✅ Да",
    "btn_extra_no": "❌ Нет",
    "calc_extra_type": "💸 *Выберите тип досрочного погашения:*",
    "btn_extra_once": "💰 Разово",
    "btn_extra_period": "📅 Период",
    "btn_extra_recurring": "🔄 Ежемесячно (весь срок)",
    "calc_extra_amount": "💸 Введите *сумму досрочного платежа* (например: 10000):",
    "calc_extra_monthly": "💸 Введите *сумму ежемесячного досрочного платежа* (например: 10000):",

    "calc_reduction_type": "🎯 *Как применять досрочное погашение?*",
    "btn_reduce_payment": "📉 Уменьшать платеж",
    "btn_reduce_term": "⏱ Уменьшать срок",
    "reduce_payment_info": "_Срок остаётся прежним, платёж уменьшается_",
    "reduce_term_info": "_Платёж остаётся прежним, срок сокращается_",

    # Results
    "results_title": "📊 *Результаты расчёта*",
    "results_loan_info": """💰 Сумма кредита: {principal:,.0f} ₽
📈 Ставка: {rate}%
📅 Срок: {months} мес.
📊 Тип: {payment_type}""",
    "results_insurance": "💼 Страховка: {insurance:,.0f} ₽/мес",
    "results_extra": """💸 Досрочный платёж: {extra:,.0f} ₽/мес
🎯 Способ: {reduction}""",
    "results_summary": "*💳 Итого:*",
    "results_monthly": "💵 Ежемесячный платёж: {payment:,.0f} ₽",
    "results_total": "📊 Общая сумма: {total:,.0f} ₽",
    "results_overpayment": "📉 Переплата: {overpayment:,.0f} ₽",
    "results_actual_months": "⏱ Фактический срок: {months} мес.",
    "results_saved_months": "⚡️ Сэкономлено: {saved} месяцев",
    "results_saved_money": "💰 Экономия: {saved:,.0f} ₽",
    "btn_save_loan": "💾 Сохранить кредит",

    # Loan saved
    "loan_saved": """✅ *Кредит сохранён!*

📝 Название: {name}
💰 Сумма: {amount:,.0f} ₽

Используйте \"📊 Мои кредиты\" для просмотра.""",

    # My Loans
    "my_loans_title": "📊 *Мои кредиты*",
    "my_loans_empty": """У вас пока нет сохранённых кредитов.

Используйте \"💳 Новый расчёт\" для создания.""",

    "loan_item": """📝 *{name}*
💰 Сумма: {amount:,.0f} ₽
📈 Ставка: {rate}%
📅 Срок: {months} мес.
💳 Платёж: {payment:,.0f} ₽/мес""",

    "loan_menu_title": "⚙️ *Управление кредитом*",
    "btn_loan_schedule": "📅 График платежей",
    "btn_loan_add_payment": "💸 Добавить платёж",
    "btn_loan_back_list": "📊 К списку кредитов",

    "schedule_title": "📅 *График платежей* — {name}",
    "schedule_header": "№ | Дата | Платёж | Тело | % | Остаток",
    "schedule_row": "{n:>2} | {date} | {payment:>8,.0f} | {principal:>8,.0f} | {interest:>6,.0f} | {balance:>9,.0f}",
    "schedule_page_info": "Страница {page}/{pages}",
    "schedule_empty": "Для этого кредита график ещё не рассчитан.",

    "add_payment_prompt_amount": "💸 Введите сумму дополнительного платежа (например 10000):",
    "add_payment_prompt_month": "📅 Введите номер месяца, к которому относится платёж (1 = первый месяц):",
    "add_payment_saved": "✅ Платёж {amount:,.0f} ₽ для месяца {month} добавлен. График и итоги пересчитаны.",
    "add_payment_cancelled": "❌ Добавление платежа отменено.",

    # Edit Loan
    "edit_loan_title": """✏️ *Редактирование кредита* — {name}

Выберите, что вы хотите изменить:""",
    "btn_edit_name": "📝 Название",
    "btn_edit_amount": "💰 Сумма",
    "btn_edit_rate": "📈 Ставка",
    "btn_edit_term": "📅 Срок",
    "edit_name_prompt": "📝 Введите новое *название* кредита:",
    "edit_amount_prompt": "💰 Введите новую *сумму* кредита:",
    "edit_rate_prompt": "📈 Введите новую *процентную ставку*:",
    "edit_term_prompt": "📅 Введите новый *срок* в месяцах:",
    "edit_success": "✅ Параметр \"{field}\" успешно изменён на: *{value}*",
    "edit_cancelled": "❌ Редактирование отменено.",

    # Settings
    "settings_title": "⚙️ *Настройки*",
    "settings_language": "🌐 Язык: {lang}",
    "settings_reminders": "🔔 Напоминания: {status}",
    "settings_reminder_days": "📅 За {days} дней до платежа",
    "btn_change_language": "🌐 Изменить язык",
    "btn_toggle_reminders": "🔔 Напоминания: {status}",
    "btn_reminder_days": "📅 Изменить период",

    "language_select": "🌐 *Выберите язык:*",
    "btn_lang_ru": "🇷🇺 Русский",
    "btn_lang_en": "🇬🇧 English",
    "btn_lang_hy": "🇦🇲 Հայերեն",
    "language_changed": "✅ Язык изменён на {lang}",

    "reminders_on": "✅ Напоминания включены",
    "reminders_off": "❌ Напоминания выключены",

    # Help
    "help_text": """📖 *Справка*

*Команды:*
/start - Главное меню
/help - Эта справка
/myloans - Список кредитов

*Функции:*
💳 *Новый расчёт* - Рассчитать кредит с учётом:
• Аннуитетных или дифференцированных платежей
• Страховки
• Досрочных погашений (разово/период/ежемесячно)
• Стратегии погашения (уменьшать платёж/срок)

📊 *Мои кредиты* - Список сохранённых кредитов
⚙️ *Настройки* - Язык и уведомления
🔔 *Напоминания* - Бот напомнит о платежах""",

    # Errors
    "error_invalid_amount": "❌ Неверная сумма. Введите число больше 0:",
    "error_invalid_rate": "❌ Неверная ставка. Введите число от 0 до 100:",
    "error_invalid_term": "❌ Неверный срок. Введите число от 1 до 600:",
    "error_invalid_number": "❌ Неверный формат. Введите число:",
    "error_generic": "❌ Произошла ошибка. Попробуйте позже.",

    # Payment types
    "payment_annuity": "Аннуитетный",
    "payment_differentiated": "Дифференцированный",

    # Reduction types
    "reduction_payment": "Уменьшать платеж",
    "reduction_term": "Уменьшать срок",

    # Extra payment types
    "extra_once": "Разовый платёж",
    "extra_period": "Период",
    "extra_recurring": "Ежемесячно",

    # Loan name template
    "loan_name_template": "Кредит",

    # Status
    "on": "Вкл",
    "off": "Выкл",
}
