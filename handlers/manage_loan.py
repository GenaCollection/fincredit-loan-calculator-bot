\"\"\"Handler for managing and editing saved loans\"\"\"
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
from database.models import User, Loan, PaymentType
from localization import get_text
import logging

logger = logging.getLogger(__name__)

# States
EDIT_CHOICE, EDIT_VALUE = range(2)

async def start_edit_loan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    \"\"\"Start edit loan flow\"\"\"
    query = update.callback_query
    await query.answer()
    
    # query.data: edit_loan_<id>
    loan_id = int(query.data.split('_')[2])
    context.user_data['edit_loan_id'] = loan_id
    
    user = query.from_user
    text = get_text(user.id, 'edit_loan_title')
    
    keyboard = [
        [InlineKeyboardButton(get_text(user.id, 'btn_edit_name'), callback_data=\"edit_field_name\")],
        [InlineKeyboardButton(get_text(user.id, 'btn_edit_amount'), callback_data=\"edit_field_amount\")],
        [InlineKeyboardButton(get_text(user.id, 'btn_edit_rate'), callback_data=\"edit_field_rate\")],
        [InlineKeyboardButton(get_text(user.id, 'btn_edit_term'), callback_data=\"edit_field_term\")],
        [InlineKeyboardButton(get_text(user.id, 'btn_cancel'), callback_data=\"cancel_edit\")]
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
    \"\"\"Receive which field to edit\"\"\"
    query = update.callback_query
    await query.answer()
    
    field = query.data.split('_')[2]
    context.user_data['edit_field'] = field
    
    user = query.from_user
    prompt_key = f'prompt_edit_{field}'
    
    try:
        await query.edit_message_text(
            get_text(user.id, prompt_key),
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(get_text(user.id, 'btn_cancel'), callback_data=\"cancel_edit\")
            ]]),
            parse_mode='Markdown'
        )
    except telegram.error.BadRequest: pass
    
    return EDIT_VALUE

async def receive_new_value(update: Update, context: ContextTypes.DEFAULT_TYPE):
    \"\"\"Receive new value and update DB\"\"\"
    user = update.message.from_user
    field = context.user_data.get('edit_field')
    loan_id = context.user_data.get('edit_loan_id')
    new_value_raw = update.message.text.strip()
    
    session = get_session()
    try:
        loan = session.query(Loan).filter_by(id=loan_id).first()
        if not loan:
            await update.message.reply_text(get_text(user.id, 'error_generic'))
            return ConversationHandler.END
            
        if field == 'name':
            loan.name = new_value_raw
        elif field == 'amount':
            loan.principal = float(new_value_raw.replace(' ', '').replace(',', '.'))
        elif field == 'rate':
            loan.annual_rate = float(new_value_raw.replace(',', '.'))
        elif field == 'term':
            loan.months = int(new_value_raw)
            
        session.commit()
        
        await update.message.reply_text(
            get_text(user.id, 'edit_success'),
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(get_text(user.id, 'btn_back'), callback_data=f\"loan_{loan_id}\")
            ]]),
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f\"Error editing loan: {e}\")
        await update.message.reply_text(get_text(user.id, 'error_invalid_number'))
        return EDIT_VALUE
    finally:
        session.close()
        
    return ConversationHandler.END

async def cancel_edit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    \"\"\"Cancel edit\"\"\"
    query = update.callback_query
    await query.answer()
    loan_id = context.user_data.get('edit_loan_id')
    
    # We can't easily return to the loan menu from here because button_callback expects a specific format
    # but we can end the conversation and let the user click buttons again
    try:
        await query.edit_message_text(
            get_text(query.from_user.id, 'edit_cancelled'),
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(get_text(query.from_user.id, 'btn_back'), callback_data=f\"loan_{loan_id}\")
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
    name=\"edit_loan_conversation\",
    persistent=False
)
