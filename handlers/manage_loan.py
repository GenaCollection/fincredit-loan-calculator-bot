"""Handler for managing and editing saved loans"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes, 
    ConversationHandler, 
    CallbackQueryHandler, 
    MessageHandler,
    filters
)
import telegram.error
from database import get_session
from database.models import ExtraPayment, Loan, User
from database.operations import get_loan_for_user
from utils.loan_schedule import build_schedule_for_loan, refresh_loan_cached_totals
from localization import get_text, get_user_language
import logging

logger = logging.getLogger(__name__)

# States
EDIT_CHOICE, EDIT_VALUE = range(2)

async def start_edit_loan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start edit loan flow"""
    query = update.callback_query
    await query.answer()
    
    # query.data: edit_loan_<id>
    loan_id = int(query.data.split('_')[2])
    context.user_data['edit_loan_id'] = loan_id
    
    user_id = query.from_user.id
    lang = get_user_language(user_id)
    
    # Get loan name for title
    session = get_session()
    loan = session.query(Loan).filter_by(id=loan_id).first()
    loan_name = loan.name if loan else ""
    session.close()
    
    text = get_text(lang, 'edit_loan_title').format(name=loan_name)
    
    keyboard = [
        [InlineKeyboardButton(get_text(lang, 'btn_edit_name'), callback_data="edit_field_name")],
        [InlineKeyboardButton(get_text(lang, 'btn_edit_amount'), callback_data="edit_field_amount")],
        [InlineKeyboardButton(get_text(lang, 'btn_edit_rate'), callback_data="edit_field_rate")],
        [InlineKeyboardButton(get_text(lang, 'btn_edit_term'), callback_data="edit_field_term")],
        [InlineKeyboardButton(get_text(lang, 'btn_cancel'), callback_data="cancel_edit")]
    ]
    
    try:
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    except telegram.error.BadRequest: pass
    
    return EDIT_CHOICE

async def receive_edit_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive which field to edit"""
    query = update.callback_query
    await query.answer()
    
    field = query.data.split('_')[2]
    context.user_data['edit_field'] = field
    
    user_id = query.from_user.id
    lang = get_user_language(user_id)
    prompt_key = f'edit_{field}_prompt'
    
    try:
        await query.edit_message_text(
            get_text(lang, prompt_key),
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(get_text(lang, 'btn_cancel'), callback_data="cancel_edit")
            ]]),
            parse_mode='Markdown'
        )
    except telegram.error.BadRequest: pass
    
    return EDIT_VALUE

async def receive_new_value(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive new value and update DB"""
    user_id = update.message.from_user.id
    lang = get_user_language(user_id)
    field = context.user_data.get('edit_field')
    loan_id = context.user_data.get('edit_loan_id')
    new_value_raw = update.message.text.strip()
    
    session = get_session()
    try:
        loan = (
            session.query(Loan)
            .join(User, Loan.user_id == User.id)
            .filter(User.telegram_id == user_id, Loan.id == loan_id)
            .first()
        )
        if not loan:
            await update.message.reply_text(get_text(lang, 'error_generic'))
            return ConversationHandler.END
        
        display_field = ""
        display_value = new_value_raw
        
        if field == 'name':
            loan.name = new_value_raw
            display_field = get_text(lang, 'btn_edit_name')
        elif field == 'amount':
            loan.principal = float(new_value_raw.replace(' ', '').replace(',', '.'))
            display_field = get_text(lang, 'btn_edit_amount')
            display_value = f"{loan.principal:,.0f} ₽"
        elif field == 'rate':
            loan.annual_rate = float(new_value_raw.replace(',', '.'))
            display_field = get_text(lang, 'btn_edit_rate')
            display_value = f"{loan.annual_rate}%"
        elif field == 'term':
            loan.months = int(new_value_raw)
            display_field = get_text(lang, 'btn_edit_term')
            display_value = f"{loan.months} мес."

        if field != 'name':
            extras = session.query(ExtraPayment).filter_by(loan_id=loan.id).all()
            schedule = build_schedule_for_loan(loan, extras)
            refresh_loan_cached_totals(session, loan, schedule)

        session.commit()
        
        await update.message.reply_text(
            get_text(lang, 'edit_success').format(field=display_field, value=display_value),
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(get_text(lang, 'btn_back'), callback_data=f"view_loan_{loan_id}")
            ]]),
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"Error editing loan: {e}")
        await update.message.reply_text(get_text(lang, 'error_invalid_number'))
        return EDIT_VALUE
    finally:
        session.close()
    
    return ConversationHandler.END

async def cancel_edit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel edit"""
    query = update.callback_query
    await query.answer()
    loan_id = context.user_data.get('edit_loan_id')
    user_id = query.from_user.id
    lang = get_user_language(user_id)
    
    try:
        await query.edit_message_text(
            get_text(lang, 'edit_cancelled'),
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(get_text(lang, 'btn_back'), callback_data=f"view_loan_{loan_id}")
            ]])
        )
    except telegram.error.BadRequest: pass
    return ConversationHandler.END

edit_loan_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(start_edit_loan, pattern='^edit_loan_')],
    states={
        EDIT_CHOICE: [CallbackQueryHandler(receive_edit_choice, pattern='^edit_field_')],
        EDIT_VALUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_new_value)],
    },
    fallbacks=[CallbackQueryHandler(cancel_edit, pattern='^cancel_edit$')],
    name="edit_loan_conversation",
    persistent=False
)
