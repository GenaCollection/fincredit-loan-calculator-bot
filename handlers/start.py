from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
import logging
from database import get_user_loans, get_loan_for_user, delete_loan
from localization import get_text, get_user_language
from handlers.settings import settings_command
import telegram

logger = logging.getLogger(__name__)

def get_main_menu_keyboard(lang):
    keyboard = [
        [InlineKeyboardButton(get_text(lang, 'btn_new_calc'), callback_data='new_calc')],
        [InlineKeyboardButton(get_text(lang, 'btn_my_loans'), callback_data='my_loans')],
        [
            InlineKeyboardButton(get_text(lang, 'btn_help'), callback_data='help'),
            InlineKeyboardButton(get_text(lang, 'btn_settings'), callback_data='settings')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_reply_keyboard(lang):
    keyboard = [
        [get_text(lang, 'btn_new_calc'), get_text(lang, 'btn_my_loans')],
        [get_text(lang, 'btn_help'), get_text(lang, 'btn_settings')]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_user_language(user_id)

    await update.message.reply_text(
        get_text(lang, 'welcome'),
        reply_markup=get_reply_keyboard(lang),
        parse_mode='Markdown'
    )

    await update.message.reply_text(
        get_text(lang, 'main_menu'),
        reply_markup=get_main_menu_keyboard(lang),
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    text = get_text(lang, 'help_text')

    if update.callback_query:
        try:
            await update.callback_query.edit_message_text(
                text,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(get_text(lang, 'btn_back'), callback_data='main_menu')]]),
                parse_mode='Markdown'
            )
        except telegram.error.BadRequest:
            pass
    else:
        await update.message.reply_text(text, parse_mode='Markdown')

async def myloans_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_my_loans(update, context)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    data = query.data

    if data == 'main_menu':
        try:
            await query.edit_message_text(
                get_text(lang, 'main_menu'),
                reply_markup=get_main_menu_keyboard(lang),
                parse_mode='Markdown'
            )
        except telegram.error.BadRequest:
            pass

    elif data == 'my_loans':
        await show_my_loans(update, context)

    elif data.startswith('view_loan_'):
        loan_id = int(data.split('_')[2])
        await show_loan_details(update, context, loan_id)

    elif data.startswith('delete_loan_'):
        loan_id = int(data.split('_')[2])
        delete_loan(loan_id)
        await show_my_loans(update, context)

    elif data == 'help':
        await help_command(update, context)

    elif data == 'settings':
        await show_settings(update, context)

async def show_my_loans(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    loans = get_user_loans(user_id)

    if not loans:
        text = get_text(lang, 'my_loans_empty')
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(get_text(lang, 'btn_back'), callback_data='main_menu')]])
    else:
        text = get_text(lang, 'my_loans_title')
        keyboard = []
        for loan in loans:
            keyboard.append([InlineKeyboardButton(f"📝 {loan.name}", callback_data=f"view_loan_{loan.id}")])
        keyboard.append([InlineKeyboardButton(get_text(lang, 'btn_back'), callback_data='main_menu')])
        reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        if update.callback_query:
            await update.callback_query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
        else:
            await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    except telegram.error.BadRequest:
        pass

async def show_loan_details(update: Update, context: ContextTypes.DEFAULT_TYPE, loan_id: int):
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    loan = get_loan_for_user(user_id, loan_id)

    if not loan:
        return

    text = get_text(lang, 'loan_item').format(
        name=loan.name,
        amount=loan.principal,
        rate=loan.annual_rate,
        months=loan.months,
        payment=loan.monthly_payment or 0
    )
    text += get_text(lang, 'loan_menu_title')

    keyboard = [
        [InlineKeyboardButton(get_text(lang, 'btn_loan_schedule'), callback_data=f"loan_schedule_{loan.id}_1")],
        [InlineKeyboardButton(get_text(lang, 'btn_loan_add_payment'), callback_data=f"add_payment_{loan.id}")],
        [InlineKeyboardButton(get_text(lang, 'btn_edit'), callback_data=f"edit_loan_{loan.id}")],
        [InlineKeyboardButton(get_text(lang, 'btn_delete'), callback_data=f"delete_loan_{loan.id}")],
        [InlineKeyboardButton(get_text(lang, 'btn_loan_back_list'), callback_data='my_loans')]
    ]

    try:
        await update.callback_query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    except telegram.error.BadRequest:
        pass

async def show_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_user_language(user_id)

    text = get_text(lang, 'settings_title')

    keyboard = [
        [InlineKeyboardButton(get_text(lang, 'btn_change_language'), callback_data='change_lang')],
        [InlineKeyboardButton(get_text(lang, 'btn_back'), callback_data='main_menu')]
    ]

    try:
        await update.callback_query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    except telegram.error.BadRequest:
        pass

async def route_text_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reply-клавиатура и прочие текстовые сообщения (не команды)."""
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    text = (update.message.text or '').strip()

    if text == get_text(lang, 'btn_my_loans'):
        await show_my_loans(update, context)
        return
    if text == get_text(lang, 'btn_settings'):
        await settings_command(update, context)
        return
    if text == get_text(lang, 'btn_help'):
        await help_command(update, context)
        return

    await handle_add_payment_message(update, context)

async def handle_add_payment_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass
