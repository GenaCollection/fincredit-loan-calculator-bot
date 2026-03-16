"""Armenian localization - Հայերեն տեքստեր"""

TEXTS = {
    # Welcome & Menu
    'welcome': '🎉 Բարի գալուստ *FinCredit*!\n\n'
               '💰 Ես կօգնեմ Ձեզ:\n'
               '✅ Հաշվարկել վարկ վաղաժամ մարումներով\n'
               '✅ Հաշվի առնել ապահովագրությունը\n'
               '✅ Համեմատել մարման ռազմավարությունները\n'
               '✅ Պահպանել և հետևել վարկերին\n'
               '✅ Ստանալ վճարումների հիշեցումներ\n\n'
               'Ընտրեք գործողություն:',
    
    'main_menu': '📋 *Գլխավոր ընտրացանկ*',
    
    # Buttons
    'btn_new_calc': '💳 Նոր հաշվարկ',
    'btn_my_loans': '📊 Իմ վարկերը',
    'btn_help': '❓ Օգնություն',
    'btn_settings': '⚙️ Կարգավորումներ',
    'btn_back': '◀️ Հետ',
    'btn_cancel': '❌ Չեղարկել',
    'btn_save': '💾 Պահպանել',
    'btn_delete': '🗑 Ջնջել',
    'btn_edit': '✏️ Խմբագրել',
    'btn_view_schedule': '📅 Վճարումների գրաֆիկ',
    'btn_add_extra': '💸 Վաղաժամ վճարում',
    
    # Calculator
    'calc_start': '💳 *Վարկի հաշվիչ*\n\n'
                  'Եկեք հաշվարկենք Ձեր վարկը!\n\n'
                  '📝 Մուտքագրեք *վարկի գումարը* (օրինակ՝ 1000000):',
    
    'calc_amount_set': '✅ Գումար: {amount:,.0f} ₽\n\n'
                       '📈 Մուտքագրեք *տոկոսադրույքը* (օրինակ՝ 12.5):',
    
    'calc_rate_set': '✅ Տոկոս: {rate}%\n\n'
                     '📅 Մուտքագրեք *ժամկետը ամիսներով* (օրինակ՝ 24):',
    
    'calc_term_set': '✅ Ժամկետ: {months} ամիս\n\n'
                     '📊 Ընտրեք *վճարման տեսակը*:',
    
    'calc_payment_type': '💳 Ընտրեք վճարման տեսակը:',
    'btn_annuity': '📊 Անուիտետային',
    'btn_differentiated': '📉 Դիֆերենցված',
    'annuity_info': '_Հավասար վճարումներ ամեն ամիս_',
    'diff_info': '_Վճարումները նվազում են ժամանակի ընթացքում_',
    
    'calc_insurance': '💼 *Ապահովագրություն*\n\n'
                      'Կվճարե՞ք ամսական ապահովագրություն:',
    'btn_insurance_yes': '✅ Այո, հաշվի առնել',
    'btn_insurance_no': '❌ Ոչ',
    
    'calc_insurance_amount': '💼 Մուտքագրեք *ամսական ապահովագրության գումարը* (օրինակ՝ 1500):',
    
    'calc_extra_payments': '💸 *Վաղաժամ մարում*\n\n'
                          'Պլանավորու՞մ եք վաղաժամ վճարումներ:',
    'btn_extra_yes': '✅ Այո',
    'btn_extra_no': '❌ Ոչ',
    
    'calc_extra_type': '💸 *Ընտրեք վաղաժամ մարման տեսակը:*',
    'btn_extra_once': '💰 Մեկանգամյա',
    'btn_extra_period': '📅 Ժամանակաշրջան',
    'btn_extra_recurring': '🔄 Ամսական (ամբողջ ժամկետը)',
    
    'calc_extra_amount': '💸 Մուտքագրեք *վաղաժամ վճարման գումարը* (օրինակ՝ 10000):',
    'calc_extra_monthly': '💸 Մուտքագրեք *ամսական լրացուցիչ վճարման գումարը* (օրինակ՝ 10000):',
    
    'calc_reduction_type': '🎯 *Ինչպե՞ս կիրառել վաղաժամ մարումը:*',
    'btn_reduce_payment': '📉 Նվազեցնել վճարումը',
    'btn_reduce_term': '⏱ Նվազեցնել ժամկետը',
    'reduce_payment_info': '_Ժամկետը մնում է նույնը, վճարումը նվազում է_',
    'reduce_term_info': '_Վճարումը մնում է նույնը, ժամկետը կարճանում է_',
    
    # Results
    'results_title': '📊 *Հաշվարկի արդյունքներ*\n\n',
    'results_loan_info': '💰 Վարկի գումար: {principal:,.0f} ₽\n'
                        '📈 Տոկոս: {rate}%\n'
                        '📅 Ժամկետ: {months} ամիս\n'
                        '📊 Տեսակ: {payment_type}\n',
    
    'results_insurance': '💼 Ապահովագրություն: {insurance:,.0f} ₽/ամիս\n',
    'results_extra': '💸 Վաղաժամ վճարում: {extra:,.0f} ₽/ամիս\n'
                    '🎯 Մեթոդ: {reduction}\n',
    
    'results_summary': '\n*💳 Ընդամենը:*\n',
    'results_monthly': '💵 Ամսական վճարում: {payment:,.0f} ₽\n',
    'results_total': '📊 Ընդհանուր գումար: {total:,.0f} ₽\n',
    'results_overpayment': '📉 Գերավճար: {overpayment:,.0f} ₽\n',
    'results_actual_months': '⏱ Փաստացի ժամկետ: {months} ամիս\n',
    'results_saved_months': '⚡️ Խնայված: {saved} ամիս\n',
    'results_saved_money': '💰 Խնայողություն: {saved:,.0f} ₽',
    
    'btn_save_loan': '💾 Պահպանել վարկը',
    'btn_new_calc': '🔄 Նոր հաշվարկ',
    
    # Loan saved
    'loan_saved': '✅ *Վարկը պահպանված է!*\n\n'
                  '📝 Անուն: {name}\n'
                  '💰 Գումար: {amount:,.0f} ₽\n\n'
                  'Օգտագործեք "📊 Իմ վարկերը" դիտելու համար:',
    
    # My Loans
    'my_loans_title': '📊 *Իմ վարկերը*\n\n',
    'my_loans_empty': 'Դուք դեռ չունեք պահպանված վարկեր:\n\n'
                      'Օգտագործեք "💳 Նոր հաշվարկ" ստեղծելու համար:',
    
    'loan_item': '📝 *{name}*\n'
                 '💰 Գումար: {amount:,.0f} ₽\n'
                 '📈 Տոկոս: {rate}%\n'
                 '📅 Ժամկետ: {months} ամիս\n'
                 '💳 Վճարում: {payment:,.0f} ₽/ամիս\n',
    
    # Settings
    'settings_title': '⚙️ *Կարգավորումներ*\n\n',
    'settings_language': '🌐 Լեզու: {lang}\n',
    'settings_reminders': '🔔 Հիշեցումներ: {status}\n',
    'settings_reminder_days': '📅 {days} օր առաջ վճարումից\n',
    
    'btn_change_language': '🌐 Փոխել լեզուն',
    'btn_toggle_reminders': '🔔 Հիշեցումներ: {status}',
    'btn_reminder_days': '📅 Փոխել ժամանակահատվածը',
    
    'language_select': '🌐 *Ընտրեք լեզուն:*',
    'btn_lang_ru': '🇷🇺 Русский',
    'btn_lang_en': '🇬🇧 English',
    'btn_lang_hy': '🇦🇲 Հայերեն',
    
    'language_changed': '✅ Լեզուն փոխվել է հայերենի',
    'reminders_on': '✅ Հիշեցումներն ակտիվացված են',
    'reminders_off': '❌ Հիշեցումներն անջատված են',
    
    # Help
    'help_text': '📖 *Օգնություն*\n\n'
                 '*Հրամաններ:*\n'
                 '/start - Գլխավոր ընտրացանկ\n'
                 '/help - Այս օգնությունը\n'
                 '/myloans - Վարկերի ցանկ\n\n'
                 '*Գործառույթներ:*\n'
                 '💳 *Նոր հաշվարկ* - Հաշվարկել վարկ՝\n'
                 '  • Անուիտետային կամ դիֆերենցված վճարումներով\n'
                 '  • Ապահովագրությամբ\n'
                 '  • Վաղաժամ մարումներով (մեկանգամյա/ժամանակաշրջան/ամսական)\n'
                 '  • Մարման ռազմավարությամբ (նվազեցնել վճարումը/ժամկետը)\n\n'
                 '📊 *Իմ վարկերը* - Պահպանված վարկերի ցանկ\n'
                 '⚙️ *Կարգավորումներ* - Լեզուն և ծանուցումները\n\n'
                 '🔔 *Հիշեցումներ* - Բոտը կհիշեցնի վճարումների մասին',
    
    # Errors
    'error_invalid_amount': '❌ Անվավեր գումար: Մուտքագրեք 0-ից մեծ թիվ:',
    'error_invalid_rate': '❌ Անվավեր տոկոս: Մուտքագրեք 0-ից 100 թիվ:',
    'error_invalid_term': '❌ Անվավեր ժամկետ: Մուտքագրեք 1-ից 600 թիվ:',
    'error_invalid_number': '❌ Անվավեր ձևաչափ: Մուտքագրեք թիվ:',
    'error_generic': '❌ Սխալ է տեղի ունեցել: Փորձեք ավելի ուշ:',
    
    # Payment types
    'payment_annuity': 'Անուիտետային',
    'payment_differentiated': 'Դիֆերենցված',
    
    # Reduction types  
    'reduction_payment': 'Նվազեցնել վճարումը',
    'reduction_term': 'Նվազեցնել ժամկետը',
    
    # Extra payment types
    'extra_once': 'Մեկանգամյա վճարում',
    'extra_period': 'Ժամանակաշրջան',
    'extra_recurring': 'Ամսական',
    
    # Status
    'on': 'Միացված',
    'off': 'Անջատված',
}
