"""Добавление разового досрочного платежа к сохранённому кредиту."""
import logging
import re

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from database import get_session
from database.models import ExtraPayment, ExtraPaymentType, Loan, User
from localization import get_text, get_user_language
from utils.loan_schedule import build_schedule_for_loan, refresh_loan_cached_totals

logger = logging.getLogger(__name__)

ADD_AMOUNT, ADD_MONTH = range(2)


def _parse_float(s: str) -> float:
    return float(re.sub(r"\s", "", s).replace(",", "."))


def _parse_int(s: str) -> int:
    return int(re.sub(r"\s", "", s))


async def start_add_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lang = get_user_language(user_id)

    try:
        loan_id = int(query.data.split("_")[2])
    except (IndexError, ValueError):
        return ConversationHandler.END

    context.user_data["add_payment_loan_id"] = loan_id

    session = get_session()
    try:
        loan = (
            session.query(Loan)
            .join(User, Loan.user_id == User.id)
            .filter(User.telegram_id == user_id, Loan.id == loan_id)
            .first()
        )
    finally:
        session.close()

    if not loan:
        await query.edit_message_text(get_text(lang, "error_generic"))
        return ConversationHandler.END

    try:
        await query.edit_message_text(
            get_text(lang, "add_payment_prompt_amount"),
            parse_mode="Markdown",
        )
    except telegram.error.BadRequest:
        pass

    return ADD_AMOUNT


async def receive_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    loan_id = context.user_data.get("add_payment_loan_id")

    raw = update.message.text.strip()
    try:
        amount = _parse_float(raw)
        if amount <= 0:
            raise ValueError()
    except ValueError:
        await update.message.reply_text(get_text(lang, "error_invalid_number"))
        return ADD_AMOUNT

    context.user_data["add_payment_amount"] = amount

    await update.message.reply_text(
        get_text(lang, "add_payment_prompt_month"),
        parse_mode="Markdown",
    )
    return ADD_MONTH


async def receive_month(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    loan_id = context.user_data.get("add_payment_loan_id")
    amount = context.user_data.get("add_payment_amount")

    raw = update.message.text.strip()
    try:
        month = _parse_int(raw)
        if month < 1:
            raise ValueError()
    except ValueError:
        await update.message.reply_text(get_text(lang, "error_invalid_number"))
        return ADD_MONTH

    session = get_session()
    try:
        loan = (
            session.query(Loan)
            .join(User, Loan.user_id == User.id)
            .filter(User.telegram_id == user_id, Loan.id == loan_id)
            .first()
        )
        if not loan:
            await update.message.reply_text(get_text(lang, "error_generic"))
            return ConversationHandler.END

        if month > loan.months:
            await update.message.reply_text(get_text(lang, "error_invalid_term"))
            return ADD_MONTH

        ep = ExtraPayment(
            loan_id=loan.id,
            amount=float(amount),
            payment_month=month,
            extra_type=ExtraPaymentType.ONE_TIME,
            is_applied=True,
        )
        session.add(ep)
        session.flush()

        extras = session.query(ExtraPayment).filter_by(loan_id=loan.id).all()
        schedule = build_schedule_for_loan(loan, extras)
        refresh_loan_cached_totals(session, loan, schedule)
        session.commit()

        await update.message.reply_text(
            get_text(lang, "add_payment_saved", amount=amount, month=month),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            get_text(lang, "btn_back"),
                            callback_data=f"view_loan_{loan_id}",
                        )
                    ]
                ]
            ),
            parse_mode="Markdown",
        )
    except Exception as e:
        logger.exception(e)
        session.rollback()
        await update.message.reply_text(get_text(lang, "error_generic"))
    finally:
        session.close()

    context.user_data.clear()
    return ConversationHandler.END


async def cancel_add_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    return ConversationHandler.END


add_payment_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(start_add_payment, pattern=r"^add_payment_\d+$")],
    states={
        ADD_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_amount)],
        ADD_MONTH: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_month)],
    },
    fallbacks=[MessageHandler(filters.Regex(r"^/(cancel|start)$"), cancel_add_payment)],
    name="add_payment",
    persistent=False,
)
