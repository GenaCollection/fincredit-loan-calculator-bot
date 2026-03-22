"""Armenian localization - Հայերեն տեքստեր"""
TEXTS = {
    # Welcome & Menu
    'welcome': """🎉 Բարի գալուստ *FinCredit*!

💰 Ես կօգնեմ Ձեզ:
✅ Հաշվարկել վարկ վաղաժամ մարումներով
✅ Հաշվի առնել ապահովագրությունը
✅ Համեմատել մարման ռազմավարությունները
✅ Պահպանել և հետևել վարկերին
✅ Ստանալ վճարումների հիշեցումներ

Ընտրեք գործողություն:""",
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
    'calc_start': """💳 *Վարկի հաշվիչ*
Եկեք հաշվարկենք Ձեր վարկը!

📝 Մուտքագրեք *վարկի գումարը* (օրինակ՝ 1000000):""",
    'calc_amount_set': '✅ Գումար: {amount:,.0f} ₽',
    'calc_rate_set': '✅ Տոկոս: {rate}%',
    'calc_term_set': '✅ Ժամկետ: {months} ամիս',
    'calc_payment_type': '💳 Ընտրեք վճարման տեսակը:',
    'btn_annuity': '📊 Անուիտետային',
    'btn_differentiated': '📉 Դիֆերենցված',
    'annuity_info': '_Հավասար վճարումներ ամեն ամիս_',
    'diff_info': '_Վճարումները նվազում են ժամանակի ընթացքում_',
    'calc_insurance': """💼 *Ապահովագրություն*
Կվճարե՞ք ամսական ապահովագրություն?""",
    'btn_insurance_yes': '✅ Այո, հաշվի առնել',
    'btn_insurance_no': '❌ Ոչ',
    'calc_insurance_amount': '💼 Մուտքագրեք *ամսական ապահովագրության գումարը* (օրինակ՝ 1500):',
    'calc_extra_payments': """💸 *Վաղաժամ մարում*
Պլանավորու՞մ եք վաղաժամ վճարումներ?""",
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
    'results_title': '📊 *Հաշվարկի արդյունքներ*',
    'results_loan_info': """💰 Վարկի գումար: {principal:,.0f} ₽
📈 Տոկոս: {rate}%
📅 Ժամկետ: {months} ամիս
📊 Տեսակ: {payment_type}""",
    'results_insurance': '💼 Ապահովագրություն: {insurance:,.0f} ₽/ամիս',
    'results_extra': """💸 Վաղաժամ վճարում: {extra:,.0f} ₽/ամիս
🎯 Մեթոդ: {reduction}""",
    'results_summary': '*💳 Ընդամենը:*',
    'results_monthly': '💵 Ամսական վճարում: {payment:,.0f} ₽',
    'results_total': '📊 Ընդհանուր գումար: {total:,.0f} ₽',
    'results_overpayment': '📉 Գերավճար: {overpayment:,.0f} ₽',
    'results_actual_months': '⏱ Փաստացի ժամկետ: {months} ամիս',
    'results_saved_months': '⚡️ Խնայված: {saved} ամիս',
    'results_saved_money': '💰 Խնայողություն: {saved:,.0f} ₽',
    'btn_save_loan': '💾 Պահպանել վարկը',
    # Loan saved
    'loan_saved': """✅ *Վարկը պահպանված է!*
📝 Անուն: {name}
💰 Գումար: {amount:,.0f} ₽
Օգտագործեք "📊 Իմ վարկերը" դիտելու համար:""",
    # My Loans
    'my_loans_title': '📊 *Իմ վարկերը*',
    'my_loans_empty': """Դուք դեռ չունեք պահպանված վարկեր:
Օգտագործեք "💳 Նոր հաշվարկ" ստեղծելու համար:""",
    'loan_item': """📝 *{name}*
💰 Գումար: {amount:,.0f} ₽
📈 Տոկոս: {rate}%
📅 Ժամկետ: {months} ամիս
💳 Վճարում: {payment:,.0f} ₽/ամիս""",
    'loan_menu_title': '⚙️ *Վարկի կառավարում*',
    'btn_loan_schedule': '📅 Վճարումների գրաֆիկ',
    'btn_loan_add_payment': '💸 Ավելացնել վճարում',
    'btn_loan_back_list': '📊 Վարկերի ցանկ',
    'schedule_title': '📅 *Վճարումների գրաֆիկ* — {name}',
    'schedule_header': '№ | Ամսաթիվ | Վճարում | Մայր գումար | % | Մնացորդ',
    'schedule_row': '{n:>2} | {date} | {payment:>8,.0f} | {principal:>8,.0f} | {interest:>6,.0f} | {balance:>9,.0f}',
    'schedule_page_info': 'Էջ {page}/{pages}',
    'schedule_empty': 'Այս վարկի համար գրաֆիկը դեռ հաշվարկված չէ:',
    'add_payment_prompt_amount': '💸 Մուտքագրեք լրացուցիչ վճարման գումարը (օրինակ՝ 10000):',
    'add_payment_prompt_month': '📅 Մուտքագրեք ամսվա համարը, որին վերաբերում է վճարումը (1 = առաջին ամիս):',
    'add_payment_saved': """✅ {amount:,.0f} ₽ վճարումը {month} ամսվա համար ավելացվել է:
Գրաֆիկը և արդյունքները վերահաշվարկվել են:""",
    'add_payment_cancelled': '❌ Վճարման ավելացումը չեղարկվել է:',
    # Edit Loan
    'edit_loan_title': """✏️ *Վարկի խմբագրում* — {name}
Ընտրեք, թե ինչ եք ցանկանում փոխել:""",
    'btn_edit_name': '📝 Անուն',
    'btn_edit_amount': '💰 Գումար',
    'btn_edit_rate': '📈 Տոկոս',
    'btn_edit_term': '📅 Ժամկետ',
    'edit_name_prompt': '📝 Մուտքագրեք նոր *անունը*:',
    'edit_amount_prompt': '💰 Մուտքագրեք նոր *գումարը*:',
    'edit_rate_prompt': '📈 Մուտքագրեք նոր *տոկոսադրույքը*:',
    'edit_term_prompt': '📅 Մուտքագրեք նոր *ժամկետը* ամիսներով:',
    'edit_success': '✅ "{field}" պարամետրը հաջողությամբ փոխվել է: *{value}*',
    'edit_cancelled': '❌ Խմբագրումը չեղարկվել է:',
    # Settings
    'settings_title': '⚙️ *Կարգավորումներ*',
    'settings_language': '🌐 Լեզու: {lang}',
    'settings_reminders': '🔔 Հիշեցումներ: {status}',
    'settings_reminder_days': '📅 {days} օր առաջ վճարումից',
    'btn_change_language': '🌐 Փոխել լեզուն',
    'btn_toggle_reminders': '🔔 Հիշեցումներ: {status}',
    'btn_reminder_days': '📅 Փոխել ժամանակահատվածը',
    'language_select': '🌐 *Ընտրեք լեզուն:*',
    'btn_lang_ru': '🇷🇺 Русский',
    'btn_lang_en': '🇬🇧 English',
    'btn_lang_hy': '🇦🇲 Հայերեն',
    'language_changed': '✅ Լեզուն փոխվել է',
    'reminders_on': '✅ Հիշեցումներն ակտիվացված են',
    'reminders_off': '❌ Հիշեցումներն անջատված են',
    # Help
    'help_text': """📖 *Օգնություն*
*Հրամաններ:*
/start - Գլխավոր ընտրացանկ
/help - Այս օգնությունը
/myloans - Վարկերի ցանկ

*Գործառույթներ:*
💳 *Նոր հաշվարկ* - Հաշվարկել վարկ՝
 • Անուիտետային կամ դիֆերենցված վճարումներով
 • Ապահովագրությամբ
 • Վաղաժամ մարումներով (մեկանգամյա/ժամանակաշրջան/ամսական)
 • Մարման ռազմավարությամբ (նվազեցնել վճարումը/ժամկետը)
📊 *Իմ վարկերը* - Պահպանված վարկերի ցանկ
⚙️ *Կարգավորումներ* - Լեզուն և ծանուցումները
🔔 *Հիշեցումներ* - Բոտը կհիշեցնի վճարումների մասին""",
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
    # Loan name template
    'loan_name_template': 'Վարկ',
    # Status
    'on': 'Միացված',
    'off': 'Անջատված',
}
