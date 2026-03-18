"""Russian localization"""
TEXTS = {
    # Welcome & Menu
    'welcome': '🎉 Добро пожаловать в *FinCredit*!\n\n'
    '💰 Я помогу вам:\n'
    '✅ Рассчитать кредит с досрочными платежами\n'
    '✅ Учесть страховку и комиссии\n'
    '✅ Сравнить стратегии погашения\n'
    '✅ Сохранить и отслеживать кредиты\n'
    '✅ Получать напоминания о платежах\n\n'
    'Выберите действие:',
    
    'main_menu': '📋 *Главное меню*',
    
    # Buttons
    'btn_new_calc': '💳 Новый расчёт',
    'btn_my_loans': '📊 Мои кредиты',
    'btn_help': '❓ Помощь',
    'btn_settings': '⚙️ Настройки',
    'btn_back': '◀️ Назад',
    'btn_cancel': '❌ Отменить',
    'btn_save': '💾 Сохранить',
    'btn_delete': '🗑 Удалить',
    'btn_edit': '✏️ Изменить',
    'btn_view_schedule': '📅 График платежей',
    'btn_add_extra': '💸 Досрочный платёж',
    
    # Calculator
    'calc_start': '💳 *Кредитный калькулятор*\n\n'
    'Давайте рассчитаем ваш кредит!\n\n'
    '📝 Введите *сумму кредита* (например: 1000000):',
    
    'calc_amount_set': '✅ Сумма: {amount:,.0f} ₽\n\n'
    '📈 Введите *процентную ставку* (например: 12.5):',
    
    'calc_rate_set': '✅ Ставка: {rate}%\n\n'
    '📅 Введите *срок кредита в месяцах* (например: 24):',
    
    'calc_term_set': '✅ Срок: {months} мес.\n\n'
    '📊 Выберите *тип платежа*:',
    
    'calc_payment_type': '💳 Выберите тип платежа:',
    'btn_annuity': '📊 Аннуитетный',
    'btn_differentiated': '📉 Дифференцированный',
    'annuity_info': '_Равные платежи каждый месяц_',
    'diff_info': '_Платежи уменьшаются со временем_',
    
    'calc_insurance': '💼 *Страховка*\n\n'
    'Будете ли вы платить ежемесячную страховку по кредиту?',
    'btn_insurance_yes': '✅ Да, учитывать',
    'btn_insurance_no': '❌ Нет',
    
    'calc_insurance_amount': '💼 Введите *сумму ежемесячной страховки* (например: 1500):',
    
    'calc_extra_payments': '💸 *Досрочное погашение*\n\n'
    'Планируете ли вы делать досрочные платежи?',
    'btn_extra_yes': '✅ Да',
    'btn_extra_no': '❌ Нет',
    
    'calc_extra_type': '💸 *Выберите тип досрочного погашения:*',
    'btn_extra_once': '💰 Разово',
    'btn_extra_period': '📅 Период',
    'btn_extra_recurring': '🔄 Ежемесячно (весь срок)',
    
    'calc_extra_amount': '💸 Введите *сумму досрочного платежа* (например: 10000):',
    'calc_extra_monthly': '💸 Введите *сумму ежемесячного досрочного платежа* (например: 10000):',
    
    'calc_reduction_type': '🎯 *Как применять досрочное погашение?*',
    'btn_reduce_payment': '📉 Уменьшать платеж',
    'btn_reduce_term': '⏱ Уменьшать срок',
    'reduce_payment_info': '_Срок остаётся прежним, платёж уменьшается_',
    'reduce_term_info': '_Платёж остаётся прежним, срок сокращается_',
    
    # Results
    'results_title': '📊 *Результаты расчёта*\n\n',
    'results_loan_info': '💰 Сумма кредита: {principal:,.0f} ₽\n'
    '📈 Ставка: {rate}%\n'
    '📅 Срок: {months} мес.\n'
    '📊 Тип: {payment_type}\n',
    
    'results_insurance': '💼 Страховка: {insurance:,.0f} ₽/мес\n',
    'results_extra': '💸 Досрочный платёж: {extra:,.0f} ₽/мес\n'
    '🎯 Способ: {reduction}\n',
    
    'results_summary': '\n*💳 Итого:*\n',
    'results_monthly': '💵 Ежемесячный платёж: {payment:,.0f} ₽\n',
    'results_total': '📊 Общая сумма: {total:,.0f} ₽\n',
    'results_overpayment': '📉 Переплата: {overpayment:,.0f} ₽\n',
    'results_actual_months': '⏱ Фактический срок: {months} мес.\n',
    'results_saved_months': '⚡️ Сэкономлено: {saved} месяцев\n',
    'results_saved_money': '💰 Экономия: {saved:,.0f} ₽',
    
    'btn_save_loan': '💾 Сохранить кредит',
    'btn_new_calc': '🔄 Новый расчёт',
    
    # Loan saved
    'loan_saved': '✅ *Кредит сохранён!*\n\n'
    '📝 Название: {name}\n'
    '💰 Сумма: {amount:,.0f} ₽\n\n'
    'Используйте "📊 Мои кредиты" для просмотра.',
    
    # My Loans
    'my_loans_title': '📊 *Мои кредиты*\n\n',
    'my_loans_empty': 'У вас пока нет сохранённых кредитов.\n\n'
    'Используйте "💳 Новый расчёт" для создания.',
    
    'loan_item': '📝 *{name}*\n'
    '💰 Сумма: {amount:,.0f} ₽\n'
    '📈 Ставка: {rate}%\n'
    '📅 Срок: {months} мес.\n'
    '💳 Платёж: {payment:,.0f} ₽/мес\n',
    'loan_menu_title': '\n\n⚙️ *Управление кредитом*',
    'btn_loan_schedule': '📅 График платежей',
    'btn_loan_add_payment': '💸 Добавить платёж',
    'btn_loan_back_list': '📊 К списку кредитов',
    'schedule_title': '📅 *График платежей* — {name}\n\n',
    'schedule_header': '№ | Дата | Платёж | Тело | % | Остаток\n',
    'schedule_row': '{n:>2} | {date} | {payment:>8,.0f} | {principal:>8,.0f} | {interest:>6,.0f} | {balance:>9,.0f}\n',
    'schedule_page_info': '\nСтраница {page}/{pages}',
    'schedule_empty': 'Для этого кредита график ещё не рассчитан.',
    'add_payment_prompt_amount': '💸 Введите сумму дополнительного платежа (например 10000):',
    'add_payment_prompt_month': '📅 Введите номер месяца, к которому относится платёж (1 = первый месяц):',
    'add_payment_saved': '✅ Платёж {amount:,.0f} ₽ для месяца {month} добавлен.\nГрафик и итоги пересчитаны.',
    'add_payment_cancelled': '❌ Добавление платежа отменено.',
    
    # Settings
    'settings_title': '⚙️ *Настройки*\n\n',
    'settings_language': '🌐 Язык: {lang}\n',
    'settings_reminders': '🔔 Напоминания: {status}\n',
    'settings_reminder_days': '📅 За {days} дней до платежа\n',
    
    'btn_change_language': '🌐 Изменить язык',
    'btn_toggle_reminders': '🔔 Напоминания: {status}',
    'btn_reminder_days': '📅 Изменить период',
    
    'language_select': '🌐 *Выберите язык:*',
    'btn_lang_ru': '🇷🇺 Русский',
    'btn_lang_en': '🇬🇧 English',
    'btn_lang_hy': '🇦🇲 Հայերեն',
    
    'language_changed': '✅ Язык изменён на {lang}',
    'reminders_on': '✅ Напоминания включены',
    'reminders_off': '❌ Напоминания выключены',
    
    # Help
    'help_text': '📖 *Справка*\n\n'
    '*Команды:*\n'
    '/start - Главное меню\n'
    '/help - Эта справка\n'
    '/myloans - Список кредитов\n\n'
    '*Функции:*\n'
    '💳 *Новый расчёт* - Рассчитать кредит с учётом:\n'
    ' • Аннуитетных или дифференцированных платежей\n'
    ' • Страховки\n'
    ' • Досрочных погашений (разово/период/ежемесячно)\n'
    ' • Стратегии погашения (уменьшать платёж/срок)\n\n'
    '📊 *Мои кредиты* - Список сохранённых кредитов\n'
    '⚙️ *Настройки* - Язык и уведомления\n\n'
    '🔔 *Напоминания* - Бот напомнит о платежах',
    
    # Errors
    'error_invalid_amount': '❌ Неверная сумма. Введите число больше 0:',
    'error_invalid_rate': '❌ Неверная ставка. Введите число от 0 до 100:',
    'error_invalid_term': '❌ Неверный срок. Введите число от 1 до 600:',
    'error_invalid_number': '❌ Неверный формат. Введите число:',
    'error_generic': '❌ Произошла ошибка. Попробуйте позже.',
    
    # Payment types
    'payment_annuity': 'Аннуитетный',
    'payment_differentiated': 'Дифференцированный',
    
    # Reduction types 
    'reduction_payment': 'Уменьшать платеж',
    'reduction_term': 'Уменьшать срок',
    
    # Extra payment types
    'extra_once': 'Разовый платёж',
    'extra_period': 'Период',
    'extra_recurring': 'Ежемесячно',
    
    # Loan name template
    'loan_name_template': 'Кредит',
    
    # Status
    'on': 'Вкл',
    'off': 'Выкл',
}
