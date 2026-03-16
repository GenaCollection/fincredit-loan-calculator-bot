"""Simple calculator handler for loan calculations"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler
from database import get_session
from database.models import User
from utils.calculations import (
    calculate_annuity_payment, 
    calculate_loan_totals,
    calculate_recurring_extra_payment_schedule
)
import logging

logger = logging.getLogger(__name__)


async def calculate_demo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Demo calculator with predefined values"""
    query = update.callback_query
    await query.answer()
    
    # Демо значения
    principal = 1000000
    annual_rate = 12.0
    months = 24
    
    # Расчет без досрочных платежей
    monthly_payment = calculate_annuity_payment(principal, annual_rate, months)
    totals = calculate_loan_totals(principal, annual_rate, months, 'annuity')
    
    # Расчет С досрочными платежами (10,000 руб/мес)
    extra_monthly = 10000
    schedule, summary = calculate_recurring_extra_payment_schedule(
        principal=principal,
        annual_rate=annual_rate,
        months=months,
        extra_monthly=extra_monthly,
        reduction_type='term',
        insurance_monthly=0.0
    )
    
    result_text = (
        f"📊 *Кредитный калькулятор (ДЕМО)*\n\n"
        f"💰 Сумма кредита: {principal:,.0f} ₽\n"
        f"📈 Процентная ставка: {annual_rate}%\n"
        f"📅 Срок: {months} месяцев\n\n"
        f"*БЕЗ досрочных платежей:*\n"
        f"💳 Ежемесячный платёж: {monthly_payment:,.0f} ₽\n"
        f"📊 Общая сумма: {totals['total_payment']:,.0f} ₽\n"
        f"📉 Переплата: {totals['overpayment']:,.0f} ₽\n\n"
        f"*С досрочными платежами ({extra_monthly:,.0f} ₽/мес):*\n"
        f"⏱ Фактический срок: {summary['actual_months']} мес.\n"
        f"⚡️ Сэкономлено: {summary['months_saved']} месяцев\n"
        f"📊 Общая сумма: {summary['total_payment']:,.0f} ₽\n"
        f"💰 Экономия: {totals['total_payment'] - summary['total_payment']:,.0f} ₽\n\n"
        f"_Функции калькулятора из t-j.ru добавлены!_"
    )
    
    keyboard = [
        [InlineKeyboardButton("🔄 Ещё раз", callback_data="new_calc")],
        [InlineKeyboardButton("◀️ Главное меню", callback_data="back_to_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        result_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


# Handler для Application API (версия 20+)
calculator_handler = CallbackQueryHandler(calculate_demo, pattern='^new_calc$')
