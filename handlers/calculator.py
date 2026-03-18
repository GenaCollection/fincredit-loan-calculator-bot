"""Full calculator handler with ConversationHandler and localization"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes, 
    ConversationHandler, 
    CallbackQueryHandler, 
    MessageHandler,
    filters
)
from database import get_session
from database.models import User, Loan, PaymentType, ReductionType, ExtraPaymentType
from utils.calculations import (
    calculate_annuity_payment,
    calculate_loan_totals,
    calculate_recurring_extra_payment_schedule
)
from localization import get_text
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Conversation states
(AMOUNT, RATE, TERM, PAYMENT_TYPE, 
 INSURANCE_CHOICE, INSURANCE_AMOUNT,
 EXTRA_CHOICE, EXTRA_TYPE, EXTRA_AMOUNT, 
 REDUCTION_TYPE, CONFIRM) = range(11)


async def start_calculator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start loan calculator wizard"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    context.user_data['loan_data'] = {}
    
    # Получаем текст на языке пользователя
    text = get_text(user.id, 'calc_start')
    btn_cancel = get_text(user.id, 'btn_cancel')
    
    keyboard = [[InlineKeyboardButton(btn_cancel, callback_data="cancel")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    
    return AMOUNT


async def receive_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive loan amount"""
    user = update.message.from_user
    
    try:
        amount = float(update.message.text.replace(' ', '').replace(',', '.'))
        if amount <= 0:
            error_text = get_text(user.id, 'error_invalid_amount')
            await update.message.reply_text(error_text)
            return AMOUNT
        
        context.user_data['loan_data']['principal'] = amount
        
        # Показываем следующий шаг
        text = get_text(user.id, 'calc_amount_set', amount=amount)
        btn_cancel = get_text(user.id, 'btn_cancel')
        
        keyboard = [[InlineKeyboardButton(btn_cancel, callback_data="cancel")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')
        return RATE
        
    except ValueError:
        error_text = get_text(user.id, 'error_invalid_number')
        await update.message.reply_text(error_text)
        return AMOUNT


async def receive_rate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive interest rate"""
    user = update.message.from_user
    
    try:
        rate = float(update.message.text.replace(',', '.'))
        if rate < 0 or rate > 100:
            error_text = get_text(user.id, 'error_invalid_rate')
            await update.message.reply_text(error_text)
            return RATE
        
        context.user_data['loan_data']['annual_rate'] = rate
        
        text = get_text(user.id, 'calc_rate_set', rate=rate)
        btn_cancel = get_text(user.id, 'btn_cancel')
        
        keyboard = [[InlineKeyboardButton(btn_cancel, callback_data="cancel")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')
        return TERM
        
    except ValueError:
        error_text = get_text(user.id, 'error_invalid_number')
        await update.message.reply_text(error_text)
        return RATE


async def receive_term(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive loan term"""
    user = update.message.from_user
    
    try:
        months = int(update.message.text)
        if months <= 0 or months > 600:
            error_text = get_text(user.id, 'error_invalid_term')
            await update.message.reply_text(error_text)
            return TERM
        
        context.user_data['loan_data']['months'] = months
        
        text = get_text(user.id, 'calc_term_set', months=months)
        text += '\n\n' + get_text(user.id, 'calc_payment_type')
        
        btn_annuity = get_text(user.id, 'btn_annuity')
        btn_diff = get_text(user.id, 'btn_differentiated')
        btn_cancel = get_text(user.id, 'btn_cancel')
        
        keyboard = [
            [InlineKeyboardButton(btn_annuity, callback_data="payment_annuity")],
            [InlineKeyboardButton(btn_diff, callback_data="payment_diff")],
            [InlineKeyboardButton(btn_cancel, callback_data="cancel")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')
        return PAYMENT_TYPE
        
    except ValueError:
        error_text = get_text(user.id, 'error_invalid_number')
        await update.message.reply_text(error_text)
        return TERM


async def receive_payment_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive payment type"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    
    if query.data == "payment_annuity":
        context.user_data['loan_data']['payment_type'] = 'annuity'
        payment_name = get_text(user.id, 'payment_annuity')
    else:
        context.user_data['loan_data']['payment_type'] = 'differentiated'
        payment_name = get_text(user.id, 'payment_differentiated')
    
    text = f"✅ {payment_name}\n\n" + get_text(user.id, 'calc_insurance')
    
    btn_yes = get_text(user.id, 'btn_insurance_yes')
    btn_no = get_text(user.id, 'btn_insurance_no')
    
    keyboard = [
        [InlineKeyboardButton(btn_yes, callback_data="insurance_yes")],
        [InlineKeyboardButton(btn_no, callback_data="insurance_no")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    return INSURANCE_CHOICE


async def receive_insurance_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive insurance choice"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    
    if query.data == "insurance_yes":
        text = get_text(user.id, 'calc_insurance_amount')
        btn_cancel = get_text(user.id, 'btn_cancel')
        
        keyboard = [[InlineKeyboardButton(btn_cancel, callback_data="cancel")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
        return INSURANCE_AMOUNT
    else:
        context.user_data['loan_data']['has_insurance'] = False
        context.user_data['loan_data']['insurance_monthly'] = 0.0
        return await ask_extra_payments(query, context)


async def receive_insurance_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive insurance amount"""
    user = update.message.from_user
    
    try:
        amount = float(update.message.text.replace(' ', '').replace(',', '.'))
        if amount < 0:
            error_text = get_text(user.id, 'error_invalid_number')
            await update.message.reply_text(error_text)
            return INSURANCE_AMOUNT
        
        context.user_data['loan_data']['has_insurance'] = True
        context.user_data['loan_data']['insurance_monthly'] = amount
        
        text = f"✅ {amount:,.0f} ₽/мес\n\n" + get_text(user.id, 'calc_extra_payments')
        
        btn_yes = get_text(user.id, 'btn_extra_yes')
        btn_no = get_text(user.id, 'btn_extra_no')
        
        keyboard = [
            [InlineKeyboardButton(btn_yes, callback_data="extra_yes")],
            [InlineKeyboardButton(btn_no, callback_data="extra_no")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')
        return EXTRA_CHOICE
        
    except ValueError:
        error_text = get_text(user.id, 'error_invalid_number')
        await update.message.reply_text(error_text)
        return INSURANCE_AMOUNT


async def ask_extra_payments(query, context):
    """Ask about extra payments"""
    user = query.from_user
    text = get_text(user.id, 'calc_extra_payments')
    
    btn_yes = get_text(user.id, 'btn_extra_yes')
    btn_no = get_text(user.id, 'btn_extra_no')
    
    keyboard = [
        [InlineKeyboardButton(btn_yes, callback_data="extra_yes")],
        [InlineKeyboardButton(btn_no, callback_data="extra_no")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    return EXTRA_CHOICE


async def receive_extra_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive extra payment choice"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    
    if query.data == "extra_no":
        context.user_data['loan_data']['has_extra_payments'] = False
        return await show_results(query, context)
    
    text = get_text(user.id, 'calc_extra_type')
    
    btn_once = get_text(user.id, 'btn_extra_once')
    btn_period = get_text(user.id, 'btn_extra_period')
    btn_recurring = get_text(user.id, 'btn_extra_recurring')
    btn_back = get_text(user.id, 'btn_back')
    
    keyboard = [
        [InlineKeyboardButton(btn_once, callback_data="extra_type_once")],
        [InlineKeyboardButton(btn_period, callback_data="extra_type_period")],
        [InlineKeyboardButton(btn_recurring, callback_data="extra_type_recurring")],
        [InlineKeyboardButton(btn_back, callback_data="extra_no")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    return EXTRA_TYPE


async def receive_extra_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive extra payment type"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    
    type_map = {
        "extra_type_once": ("once", get_text(user.id, 'extra_once')),
        "extra_type_period": ("period", get_text(user.id, 'extra_period')),
        "extra_type_recurring": ("recurring", get_text(user.id, 'extra_recurring'))
    }
    
    extra_type, type_name = type_map[query.data]
    context.user_data['loan_data']['extra_payment_type'] = extra_type
    
    text = f"✅ {type_name}\n\n" + get_text(user.id, 'calc_extra_monthly')
    btn_cancel = get_text(user.id, 'btn_cancel')
    
    keyboard = [[InlineKeyboardButton(btn_cancel, callback_data="cancel")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    return EXTRA_AMOUNT


async def receive_extra_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive extra payment amount"""
    user = update.message.from_user
    
    try:
        amount = float(update.message.text.replace(' ', '').replace(',', '.'))
        if amount <= 0:
            error_text = get_text(user.id, 'error_invalid_number')
            await update.message.reply_text(error_text)
            return EXTRA_AMOUNT
        
        context.user_data['loan_data']['has_extra_payments'] = True
        context.user_data['loan_data']['extra_payment_amount'] = amount
        
        text = f"✅ {amount:,.0f} ₽\n\n" + get_text(user.id, 'calc_reduction_type')
        
        btn_reduce_payment = get_text(user.id, 'btn_reduce_payment')
        btn_reduce_term = get_text(user.id, 'btn_reduce_term')
        
        keyboard = [
            [InlineKeyboardButton(btn_reduce_payment, callback_data="reduction_payment")],
            [InlineKeyboardButton(btn_reduce_term, callback_data="reduction_term")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')
        return REDUCTION_TYPE
        
    except ValueError:
        error_text = get_text(user.id, 'error_invalid_number')
        await update.message.reply_text(error_text)
        return EXTRA_AMOUNT


async def receive_reduction_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive reduction type"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    
    if query.data == "reduction_payment":
        context.user_data['loan_data']['reduction_type'] = 'payment'
        reduction_name = get_text(user.id, 'reduction_payment')
    else:
        context.user_data['loan_data']['reduction_type'] = 'term'
        reduction_name = get_text(user.id, 'reduction_term')
    
    context.user_data['loan_data']['reduction_name'] = reduction_name
    
    return await show_results(query, context)


async def show_results(query, context):
    """Calculate and show results"""
    user = query.from_user
    loan_data = context.user_data.get('loan_data', {})
    
    principal = loan_data['principal']
    annual_rate = loan_data['annual_rate']
    months = loan_data['months']
    payment_type_str = loan_data['payment_type']
    insurance = loan_data.get('insurance_monthly', 0.0)
    has_extra = loan_data.get('has_extra_payments', False)
    
    # Calculate schedule
    if has_extra:
        extra_amount = loan_data['extra_payment_amount']
        reduction_type = loan_data['reduction_type']
        reduction_name = loan_data.get('reduction_name', 'term')
        
        schedule, summary = calculate_recurring_extra_payment_schedule(
            principal=principal,
            annual_rate=annual_rate,
            months=months,
            extra_monthly=extra_amount,
            reduction_type=reduction_type,
            insurance_monthly=insurance
        )
        
        # Build result text with localization
        result_text = get_text(user.id, 'results_title')
        result_text += get_text(user.id, 'results_loan_info', 
                               principal=principal, 
                               rate=annual_rate, 
                               months=months,
                               payment_type=get_text(user.id, f'payment_{payment_type_str}'))
        
        if insurance > 0:
            result_text += get_text(user.id, 'results_insurance', insurance=insurance)
        
        result_text += get_text(user.id, 'results_extra', 
                               extra=extra_amount, 
                               reduction=reduction_name)
        
        result_text += get_text(user.id, 'results_summary')
        result_text += get_text(user.id, 'results_actual_months', months=summary['actual_months'])
        result_text += get_text(user.id, 'results_saved_months', saved=summary['months_saved'])
        result_text += get_text(user.id, 'results_total', total=summary['total_payment'])
        result_text += get_text(user.id, 'results_overpayment', overpayment=summary['overpayment'])
        
        # Calculate savings
        totals_no_extra = calculate_loan_totals(principal, annual_rate, months, 'annuity')
        savings = totals_no_extra['total_payment'] - summary['total_payment']
        result_text += '\n' + get_text(user.id, 'results_saved_money', saved=savings)
        
    else:
        monthly_payment = calculate_annuity_payment(principal, annual_rate, months)
        totals = calculate_loan_totals(principal, annual_rate, months, 'annuity')
        
        total_payment = totals['total_payment']
        overpayment = totals['overpayment']
        
        if insurance > 0:
            total_insurance = insurance * months
            total_payment += total_insurance
            overpayment += total_insurance
        
        result_text = get_text(user.id, 'results_title')
        result_text += get_text(user.id, 'results_loan_info',
                               principal=principal,
                               rate=annual_rate,
                               months=months,
                               payment_type=get_text(user.id, f'payment_{payment_type_str}'))
        
        if insurance > 0:
            result_text += get_text(user.id, 'results_insurance', insurance=insurance)
        
        result_text += get_text(user.id, 'results_summary')
        result_text += get_text(user.id, 'results_monthly', payment=monthly_payment + insurance)
        result_text += get_text(user.id, 'results_total', total=total_payment)
        result_text += get_text(user.id, 'results_overpayment', overpayment=overpayment)
    
    btn_save = get_text(user.id, 'btn_save_loan')
    btn_new = get_text(user.id, 'btn_new_calc')
    btn_back = get_text(user.id, 'btn_back')
    
    keyboard = [
        [InlineKeyboardButton(btn_save, callback_data="save_loan")],
        [InlineKeyboardButton(btn_new, callback_data="new_calc")],
        [InlineKeyboardButton(btn_back, callback_data="back_to_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        result_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    
    return CONFIRM

async def save_loan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save loan to database"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    loan_data = context.user_data.get('loan_data', {})
    
    session = get_session()
    try:
        db_user = session.query(User).filter_by(telegram_id=user.id).first()
        if not db_user:
            db_user = User(telegram_id=user.id, username=user.username)
            session.add(db_user)
            session.flush()
        
        loan_count = session.query(Loan).filter_by(user_id=db_user.id).count()

        principal = loan_data['principal']
        annual_rate = loan_data['annual_rate']
        months = loan_data['months']
        payment_type_str = loan_data.get('payment_type', 'annuity')
        insurance = float(loan_data.get('insurance_monthly', 0.0) or 0.0)
        has_extra = bool(loan_data.get('has_extra_payments', False))
        extra_type = loan_data.get('extra_payment_type')

        monthly_payment = None
        total_payment = None
        overpayment = None
        actual_months = None

        if has_extra and extra_type == 'recurring':
            extra_amount = float(loan_data.get('extra_payment_amount', 0.0) or 0.0)
            reduction_type = loan_data.get('reduction_type', 'term')
            schedule, summary = calculate_recurring_extra_payment_schedule(
                principal=principal,
                annual_rate=annual_rate,
                months=months,
                extra_monthly=extra_amount,
                reduction_type=reduction_type,
                insurance_monthly=insurance
            )
            if schedule:
                monthly_payment = float(schedule[0]['payment_amount'])
            total_payment = float(summary['total_payment'])
            overpayment = float(summary['overpayment'])
            actual_months = int(summary['actual_months'])
        else:
            totals = calculate_loan_totals(principal, annual_rate, months, payment_type_str)
            monthly_payment = float(totals['monthly_payment']) + insurance
            total_payment = float(totals['total_payment']) + insurance * months
            overpayment = total_payment - principal
            actual_months = months
        
        loan = Loan(
            user_id=db_user.id,
            name=f"Кредит {loan_count + 1}",
            principal=principal,
            annual_rate=annual_rate,
            months=months,
            payment_type=PaymentType.ANNUITY if loan_data.get('payment_type') == 'annuity' else PaymentType.DIFFERENTIATED,
            has_insurance=loan_data.get('has_insurance', False),
            insurance_monthly=insurance,
            has_extra_payments=loan_data.get('has_extra_payments', False),
            extra_payment_amount=loan_data.get('extra_payment_amount', 0.0),
            extra_payment_type=ExtraPaymentType.RECURRING if loan_data.get('extra_payment_type') == 'recurring' else None,
            reduction_type=ReductionType.PAYMENT if loan_data.get('reduction_type') == 'payment' else ReductionType.TERM,
            monthly_payment=monthly_payment,
            total_payment=total_payment,
            total_overpayment=overpayment,
            actual_months=actual_months,
            start_date=datetime.now()
        )
        
        session.add(loan)
        session.commit()
        
        success_text = get_text(user.id, 'loan_saved', name=loan.name, amount=loan.principal)
        btn_loans = get_text(user.id, 'btn_my_loans')
        btn_back = get_text(user.id, 'btn_back')
        
        await query.edit_message_text(
            success_text,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(btn_loans, callback_data="my_loans"),
                InlineKeyboardButton(btn_back, callback_data="back_to_menu")
            ]]),
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"Error saving loan: {e}")
        error_text = get_text(user.id, 'error_generic')
        await query.edit_message_text(error_text)
    finally:
        session.close()
    
    return ConversationHandler.END


async def cancel_calculator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel calculator"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    btn_back = get_text(user.id, 'btn_back')
    
    await query.edit_message_text(
        "❌ " + get_text(user.id, 'btn_cancel'),
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(btn_back, callback_data="back_to_menu")
        ]])
    )
    
    return ConversationHandler.END


# Create conversation handler
calculator_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(start_calculator, pattern='^new_calc$')],
    states={
        AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_amount)],
        RATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_rate)],
        TERM: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_term)],
        PAYMENT_TYPE: [CallbackQueryHandler(receive_payment_type, pattern='^payment_')],
        INSURANCE_CHOICE: [CallbackQueryHandler(receive_insurance_choice, pattern='^insurance_')],
        INSURANCE_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_insurance_amount)],
        EXTRA_CHOICE: [CallbackQueryHandler(receive_extra_choice, pattern='^extra_(yes|no)$')],
        EXTRA_TYPE: [CallbackQueryHandler(receive_extra_type, pattern='^extra_type_')],
        EXTRA_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_extra_amount)],
        REDUCTION_TYPE: [CallbackQueryHandler(receive_reduction_type, pattern='^reduction_')],
        CONFIRM: [
            CallbackQueryHandler(save_loan, pattern='^save_loan$'),
            CallbackQueryHandler(start_calculator, pattern='^new_calc$')
        ],
    },
    fallbacks=[
        CallbackQueryHandler(cancel_calculator, pattern='^cancel$'),
    ],
    name="calculator_conversation",
    persistent=False
)

