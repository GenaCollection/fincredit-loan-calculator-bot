"""English localization"""

TEXTS = {
    # Welcome & Menu
    'welcome': '🎉 Welcome to *FinCredit*!\n\n'
               '💰 I will help you:\n'
               '✅ Calculate loan with early repayments\n'
               '✅ Include insurance and fees\n'
               '✅ Compare repayment strategies\n'
               '✅ Save and track loans\n'
               '✅ Get payment reminders\n\n'
               'Choose an action:',
    
    'main_menu': '📋 *Main Menu*',
    
    # Buttons
    'btn_new_calc': '💳 New Calculation',
    'btn_my_loans': '📊 My Loans',
    'btn_help': '❓ Help',
    'btn_settings': '⚙️ Settings',
    'btn_back': '◀️ Back',
    'btn_cancel': '❌ Cancel',
    'btn_save': '💾 Save',
    'btn_delete': '🗑 Delete',
    'btn_edit': '✏️ Edit',
    'btn_view_schedule': '📅 Payment Schedule',
    'btn_add_extra': '💸 Extra Payment',
    
    # Calculator
    'calc_start': '💳 *Loan Calculator*\n\n'
                  'Let\'s calculate your loan!\n\n'
                  '📝 Enter *loan amount* (e.g. 1000000):',
    
    'calc_amount_set': '✅ Amount: {amount:,.0f} ₽\n\n'
                       '📈 Enter *interest rate* (e.g. 12.5):',
    
    'calc_rate_set': '✅ Rate: {rate}%\n\n'
                     '📅 Enter *loan term in months* (e.g. 24):',
    
    'calc_term_set': '✅ Term: {months} months\n\n'
                     '📊 Choose *payment type*:',
    
    'calc_payment_type': '💳 Choose payment type:',
    'btn_annuity': '📊 Annuity',
    'btn_differentiated': '📉 Differentiated',
    'annuity_info': '_Equal payments each month_',
    'diff_info': '_Decreasing payments over time_',
    
    'calc_insurance': '💼 *Insurance*\n\n'
                      'Will you pay monthly insurance?',
    'btn_insurance_yes': '✅ Yes, include',
    'btn_insurance_no': '❌ No',
    
    'calc_insurance_amount': '💼 Enter *monthly insurance amount* (e.g. 1500):',
    
    'calc_extra_payments': '💸 *Early Repayment*\n\n'
                          'Do you plan to make early payments?',
    'btn_extra_yes': '✅ Yes',
    'btn_extra_no': '❌ No',
    
    'calc_extra_type': '💸 *Choose early repayment type:*',
    'btn_extra_once': '💰 One-time',
    'btn_extra_period': '📅 Period',
    'btn_extra_recurring': '🔄 Monthly (entire term)',
    
    'calc_extra_amount': '💸 Enter *early payment amount* (e.g. 10000):',
    'calc_extra_monthly': '💸 Enter *monthly extra payment amount* (e.g. 10000):',
    
    'calc_reduction_type': '🎯 *How to apply early repayment?*',
    'btn_reduce_payment': '📉 Reduce payment',
    'btn_reduce_term': '⏱ Reduce term',
    'reduce_payment_info': '_Term stays same, payment decreases_',
    'reduce_term_info': '_Payment stays same, term shortens_',
    
    # Results
    'results_title': '📊 *Calculation Results*\n\n',
    'results_loan_info': '💰 Loan amount: {principal:,.0f} ₽\n'
                        '📈 Rate: {rate}%\n'
                        '📅 Term: {months} months\n'
                        '📊 Type: {payment_type}\n',
    
    'results_insurance': '💼 Insurance: {insurance:,.0f} ₽/month\n',
    'results_extra': '💸 Extra payment: {extra:,.0f} ₽/month\n'
                    '🎯 Method: {reduction}\n',
    
    'results_summary': '\n*💳 Total:*\n',
    'results_monthly': '💵 Monthly payment: {payment:,.0f} ₽\n',
    'results_total': '📊 Total amount: {total:,.0f} ₽\n',
    'results_overpayment': '📉 Overpayment: {overpayment:,.0f} ₽\n',
    'results_actual_months': '⏱ Actual term: {months} months\n',
    'results_saved_months': '⚡️ Saved: {saved} months\n',
    'results_saved_money': '💰 Savings: {saved:,.0f} ₽',
    
    'btn_save_loan': '💾 Save Loan',
    'btn_new_calc': '🔄 New Calculation',
    
    # Loan saved
    'loan_saved': '✅ *Loan Saved!*\n\n'
                  '📝 Name: {name}\n'
                  '💰 Amount: {amount:,.0f} ₽\n\n'
                  'Use "📊 My Loans" to view.',
    
    # My Loans
    'my_loans_title': '📊 *My Loans*\n\n',
    'my_loans_empty': 'You don\'t have any saved loans yet.\n\n'
                      'Use "💳 New Calculation" to create one.',
    
    'loan_item': '📝 *{name}*\n'
                 '💰 Amount: {amount:,.0f} ₽\n'
                 '📈 Rate: {rate}%\n'
                 '📅 Term: {months} months\n'
                 '💳 Payment: {payment:,.0f} ₽/month\n',
    'loan_menu_title': '\n\n⚙️ *Loan Management*',
    'btn_loan_schedule': '📅 Payment schedule',
    'btn_loan_add_payment': '💸 Add payment',
    'btn_loan_back_list': '📊 Back to loans list',
    'schedule_title': '📅 *Payment schedule* — {name}\n\n',
    'schedule_header': '№ | Date | Payment | Principal | % | Balance\n',
    'schedule_row': '{n:>2} | {date} | {payment:>8,.0f} | {principal:>8,.0f} | {interest:>6,.0f} | {balance:>9,.0f}\n',
    'schedule_page_info': '\nPage {page}/{pages}',
    'schedule_empty': 'Schedule is not calculated for this loan yet.',
    'add_payment_prompt_amount': '💸 Enter extra payment amount (e.g. 10000):',
    'add_payment_prompt_month': '📅 Enter month number this payment belongs to (1 = first month):',
    'add_payment_saved': '✅ Payment {amount:,.0f} ₽ for month {month} added.\nSchedule and totals recalculated.',
    'add_payment_cancelled': '❌ Adding payment cancelled.',
    
    # Settings
    'settings_title': '⚙️ *Settings*\n\n',
    'settings_language': '🌐 Language: {lang}\n',
    'settings_reminders': '🔔 Reminders: {status}\n',
    'settings_reminder_days': '📅 {days} days before payment\n',
    
    'btn_change_language': '🌐 Change Language',
    'btn_toggle_reminders': '🔔 Reminders: {status}',
    'btn_reminder_days': '📅 Change Period',
    
    'language_select': '🌐 *Select Language:*',
    'btn_lang_ru': '🇷🇺 Русский',
    'btn_lang_en': '🇬🇧 English',
    'btn_lang_hy': '🇦🇲 Հայերեն',
    
    'language_changed': '✅ Language changed to English',
    'reminders_on': '✅ Reminders enabled',
    'reminders_off': '❌ Reminders disabled',
    
    # Help
    'help_text': '📖 *Help*\n\n'
                 '*Commands:*\n'
                 '/start - Main menu\n'
                 '/help - This help\n'
                 '/myloans - List of loans\n\n'
                 '*Features:*\n'
                 '💳 *New Calculation* - Calculate loan with:\n'
                 '  • Annuity or differentiated payments\n'
                 '  • Insurance\n'
                 '  • Early repayments (one-time/period/monthly)\n'
                 '  • Repayment strategy (reduce payment/term)\n\n'
                 '📊 *My Loans* - List of saved loans\n'
                 '⚙️ *Settings* - Language and notifications\n\n'
                 '🔔 *Reminders* - Bot will remind about payments',
    
    # Errors
    'error_invalid_amount': '❌ Invalid amount. Enter a number greater than 0:',
    'error_invalid_rate': '❌ Invalid rate. Enter a number from 0 to 100:',
    'error_invalid_term': '❌ Invalid term. Enter a number from 1 to 600:',
    'error_invalid_number': '❌ Invalid format. Enter a number:',
    'error_generic': '❌ An error occurred. Please try later.',
    
    # Payment types
    'payment_annuity': 'Annuity',
    'payment_differentiated': 'Differentiated',
    
    # Reduction types  
    'reduction_payment': 'Reduce payment',
    'reduction_term': 'Reduce term',
    
    # Extra payment types
    'extra_once': 'One-time payment',
    'extra_period': 'Period',
    'extra_recurring': 'Monthly',
    
    # Status
    'on': 'On',
    'off': 'Off',
}
