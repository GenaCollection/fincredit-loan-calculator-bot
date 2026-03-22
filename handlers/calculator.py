"""ConversationHandler: новый расчёт кредита и сохранение в БД."""
import logging
import re
from datetime import datetime

import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from database import get_session
from database.models import ExtraPaymentType, Loan, PaymentType, ReductionType, User
from localization import get_text, get_user_language
from utils.calculations import (
    calculate_annuity_schedule_with_extras,
    calculate_differentiated_schedule,
    calculate_loan_totals,
    calculate_recurring_extra_payment_schedule,
)

logger = logging.getLogger(__name__)

AMOUNT, RATE, TERM, PAYMENT_TYPE, INSURANCE_YESNO, INSURANCE_AMT, EXTRA_YESNO, EXTRA_AMT, REDUCTION, RESULTS = range(10)


class NewCalcReplyFilter(filters.MessageFilter):
    """Текст кнопки Reply-клавиатуры «Новый расчёт» (локализованный)."""

    def filter(self, message):
        if not message or not message.text:
            return False
        uid = message.from_user.id
        lang = get_user_language(uid)
        return message.text.strip() == get_text(lang, 'btn_new_calc')


def _parse_float(s: str) -> float:
    return float(re.sub(r'\s', '', s).replace(',', '.'))


def _parse_int(s: str) -> int:
    return int(re.sub(r'\s', '', s))


async def _entry_new_calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lang = get_user_language(user_id)
    context.user_data.clear()
    try:
        await query.edit_message_text(
            get_text(lang, 'calc_start'),
            parse_mode='Markdown',
        )
    except telegram.error.BadRequest:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=get_text(lang, 'calc_start'),
            parse_mode='Markdown',
        )
    return AMOUNT


async def _entry_new_calc_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    context.user_data.clear()
    await update.message.reply_text(get_text(lang, 'calc_start'), parse_mode='Markdown')
    return AMOUNT


async def _amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    raw = update.message.text.strip()
    try:
        amount = _parse_float(raw)
        if amount <= 0:
            raise ValueError()
    except ValueError:
        await update.message.reply_text(get_text(lang, 'error_invalid_amount'))
        return AMOUNT
    context.user_data['amount'] = amount
    await update.message.reply_text(
        get_text(lang, 'calc_amount_set', amount=amount),
        parse_mode='Markdown',
    )
    return RATE


async def _rate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    raw = update.message.text.strip()
    try:
        rate = _parse_float(raw)
        if rate < 0 or rate > 100:
            raise ValueError()
    except ValueError:
        await update.message.reply_text(get_text(lang, 'error_invalid_rate'))
        return RATE
    context.user_data['rate'] = rate
    await update.message.reply_text(
        get_text(lang, 'calc_rate_set', rate=rate),
        parse_mode='Markdown',
    )
    return TERM


async def _term(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    raw = update.message.text.strip()
    try:
        months = _parse_int(raw)
        if months < 1 or months > 600:
            raise ValueError()
    except ValueError:
        await update.message.reply_text(get_text(lang, 'error_invalid_term'))
        return TERM
    context.user_data['term'] = months
    keyboard = [
        [
            InlineKeyboardButton(get_text(lang, 'btn_annuity'), callback_data='type_annuity'),
            InlineKeyboardButton(get_text(lang, 'btn_differentiated'), callback_data='type_diff'),
        ],
    ]
    await update.message.reply_text(
        get_text(lang, 'calc_term_set', months=months),
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown',
    )
    return PAYMENT_TYPE


async def _payment_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lang = get_user_language(user_id)
    if query.data == 'type_annuity':
        context.user_data['ptype'] = 'annuity'
    else:
        context.user_data['ptype'] = 'differentiated'
    await query.edit_message_text(
        get_text(lang, 'calc_insurance'),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(get_text(lang, 'btn_insurance_yes'), callback_data='ins_yes'),
                    InlineKeyboardButton(get_text(lang, 'btn_insurance_no'), callback_data='ins_no'),
                ]
            ]
        ),
        parse_mode='Markdown',
    )
    return INSURANCE_YESNO


async def _insurance_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lang = get_user_language(user_id)
    if query.data == 'ins_yes':
        await query.edit_message_text(
            get_text(lang, 'calc_insurance_amount'),
            parse_mode='Markdown',
        )
        return INSURANCE_AMT
    context.user_data['insurance_monthly'] = 0.0
    await query.edit_message_text(
        get_text(lang, 'calc_extra_payments'),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(get_text(lang, 'btn_extra_yes'), callback_data='ext_yes'),
                    InlineKeyboardButton(get_text(lang, 'btn_extra_no'), callback_data='ext_no'),
                ]
            ]
        ),
        parse_mode='Markdown',
    )
    return EXTRA_YESNO


async def _insurance_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    raw = update.message.text.strip()
    try:
        ins = _parse_float(raw)
        if ins < 0:
            raise ValueError()
    except ValueError:
        await update.message.reply_text(get_text(lang, 'error_invalid_number'))
        return INSURANCE_AMT
    context.user_data['insurance_monthly'] = ins
    await update.message.reply_text(
        get_text(lang, 'calc_extra_payments'),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(get_text(lang, 'btn_extra_yes'), callback_data='ext_yes'),
                    InlineKeyboardButton(get_text(lang, 'btn_extra_no'), callback_data='ext_no'),
                ]
            ]
        ),
        parse_mode='Markdown',
    )
    return EXTRA_YESNO


async def _extra_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lang = get_user_language(user_id)
    if query.data == 'ext_yes':
        await query.edit_message_text(
            get_text(lang, 'calc_extra_monthly'),
            parse_mode='Markdown',
        )
        return EXTRA_AMT
    context.user_data['extra_monthly'] = 0.0
    return await _show_results(update, context)


async def _extra_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    raw = update.message.text.strip()
    try:
        extra = _parse_float(raw)
        if extra < 0:
            raise ValueError()
    except ValueError:
        await update.message.reply_text(get_text(lang, 'error_invalid_number'))
        return EXTRA_AMT
    context.user_data['extra_monthly'] = extra
    if extra > 0:
        await update.message.reply_text(
            get_text(lang, 'calc_reduction_type'),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(get_text(lang, 'btn_reduce_payment'), callback_data='red_pay'),
                        InlineKeyboardButton(get_text(lang, 'btn_reduce_term'), callback_data='red_term'),
                    ]
                ]
            ),
            parse_mode='Markdown',
        )
        return REDUCTION
    return await _show_results(update, context)


async def _reduction_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'red_pay':
        context.user_data['reduction'] = 'payment'
    else:
        context.user_data['reduction'] = 'term'
    return await _show_results(update, context)


def _build_summary(user_data: dict) -> dict:
    p = float(user_data['amount'])
    r = float(user_data['rate'])
    m = int(user_data['term'])
    pt = user_data['ptype']
    ins = float(user_data.get('insurance_monthly', 0) or 0)
    em = float(user_data.get('extra_monthly', 0) or 0)
    red = user_data.get('reduction', 'term')

    if em > 0:
        schedule, summary = calculate_recurring_extra_payment_schedule(
            p,
            r,
            m,
            em,
            reduction_type='payment' if red == 'payment' else 'term',
            insurance_monthly=ins,
        )
        mp = schedule[0]['payment_amount'] if schedule else 0
        return {
            'monthly_payment': mp,
            'total_payment': summary['total_payment'],
            'overpayment': summary['overpayment'],
            'actual_months': summary['actual_months'],
        }

    if pt == 'differentiated':
        sch = calculate_differentiated_schedule(p, r, m)
        first = sch[0]['payment_amount'] if sch else 0
        base_total = sum(x['payment_amount'] for x in sch)
        ins_total = ins * len(sch) if ins else 0
        return {
            'monthly_payment': first + ins,
            'total_payment': base_total + ins_total,
            'overpayment': base_total + ins_total - p,
            'actual_months': len(sch),
        }

    if ins > 0:
        schedule, summary = calculate_annuity_schedule_with_extras(
            p, r, m, start_date=datetime.now(), extra_payments=None, reduction_type='term', insurance_monthly=ins
        )
        mp = schedule[0]['payment_amount'] if schedule else 0
        return {
            'monthly_payment': mp,
            'total_payment': summary['total_payment'],
            'overpayment': summary['overpayment'],
            'actual_months': summary['actual_months'],
        }

    t = calculate_loan_totals(p, r, m, 'annuity')
    return {
        'monthly_payment': t['monthly_payment'],
        'total_payment': t['total_payment'],
        'overpayment': t['overpayment'],
        'actual_months': m,
    }


async def _show_results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    ud = context.user_data
    summary = _build_summary(ud)

    pt_key = 'payment_annuity' if ud['ptype'] == 'annuity' else 'payment_differentiated'
    payment_label = get_text(lang, pt_key)

    text = get_text(lang, 'results_title')
    text += get_text(
        lang,
        'results_loan_info',
        principal=ud['amount'],
        rate=ud['rate'],
        months=ud['term'],
        payment_type=payment_label,
    )
    if ud.get('insurance_monthly'):
        text += get_text(lang, 'results_insurance', insurance=ud['insurance_monthly'])
    if ud.get('extra_monthly'):
        red_key = 'reduction_payment' if ud.get('reduction') == 'payment' else 'reduction_term'
        text += get_text(
            lang,
            'results_extra',
            extra=ud['extra_monthly'],
            reduction=get_text(lang, red_key),
        )
    text += get_text(lang, 'results_summary')
    text += get_text(lang, 'results_monthly', payment=summary['monthly_payment'])
    text += get_text(lang, 'results_total', total=summary['total_payment'])
    text += get_text(lang, 'results_overpayment', overpayment=summary['overpayment'])

    ud['_summary'] = summary

    keyboard = [
        [InlineKeyboardButton(get_text(lang, 'btn_save_loan'), callback_data='save_loan')],
        [InlineKeyboardButton(get_text(lang, 'btn_back'), callback_data='calc_cancel')],
    ]
    markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=markup, parse_mode='Markdown')
    else:
        await update.message.reply_text(text, reply_markup=markup, parse_mode='Markdown')
    return RESULTS


async def _save_loan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lang = get_user_language(user_id)
    ud = context.user_data
    summary = ud.get('_summary') or _build_summary(ud)

    session = get_session()
    try:
        db_user = session.query(User).filter_by(telegram_id=user_id).first()
        if not db_user:
            u = update.effective_user
            db_user = User(
                telegram_id=user_id,
                username=u.username,
                first_name=u.first_name,
                last_name=u.last_name,
                language=lang,
            )
            session.add(db_user)
            session.flush()

        ins = float(ud.get('insurance_monthly', 0) or 0)
        em = float(ud.get('extra_monthly', 0) or 0)
        red = ud.get('reduction', 'term')

        loan = Loan(
            user_id=db_user.id,
            name=get_text(lang, 'loan_name_template'),
            principal=float(ud['amount']),
            annual_rate=float(ud['rate']),
            months=int(ud['term']),
            payment_type=PaymentType.ANNUITY if ud['ptype'] == 'annuity' else PaymentType.DIFFERENTIATED,
            has_insurance=ins > 0,
            insurance_monthly=ins,
            has_extra_payments=em > 0,
            extra_payment_amount=em,
            extra_payment_type=ExtraPaymentType.RECURRING if em > 0 else None,
            reduction_type=ReductionType.PAYMENT if red == 'payment' else ReductionType.TERM,
            monthly_payment=float(summary['monthly_payment']),
            total_payment=float(summary['total_payment']),
            total_overpayment=float(summary['overpayment']),
            actual_months=int(summary.get('actual_months') or ud['term']),
        )
        session.add(loan)
        session.commit()

        await query.edit_message_text(
            get_text(
                lang,
                'loan_saved',
                name=loan.name,
                amount=loan.principal,
            ),
            parse_mode='Markdown',
        )
    except Exception as e:
        logger.exception(e)
        session.rollback()
        await query.edit_message_text(get_text(lang, 'error_generic'))
    finally:
        session.close()

    context.user_data.clear()
    return ConversationHandler.END


async def _calc_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lang = get_user_language(user_id)
    context.user_data.clear()
    from handlers.start import get_main_menu_keyboard

    try:
        await query.edit_message_text(
            get_text(lang, 'main_menu'),
            reply_markup=get_main_menu_keyboard(lang),
            parse_mode='Markdown',
        )
    except telegram.error.BadRequest:
        pass
    return ConversationHandler.END


async def _cancel_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    return ConversationHandler.END


calculator_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(_entry_new_calc, pattern=r'^new_calc$'),
        MessageHandler(
            NewCalcReplyFilter() & filters.TEXT & ~filters.COMMAND,
            _entry_new_calc_reply,
        ),
    ],
    states={
        AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, _amount)],
        RATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, _rate)],
        TERM: [MessageHandler(filters.TEXT & ~filters.COMMAND, _term)],
        PAYMENT_TYPE: [CallbackQueryHandler(_payment_type, pattern=r'^type_(annuity|diff)$')],
        INSURANCE_YESNO: [CallbackQueryHandler(_insurance_choice, pattern=r'^ins_(yes|no)$')],
        INSURANCE_AMT: [MessageHandler(filters.TEXT & ~filters.COMMAND, _insurance_amount)],
        EXTRA_YESNO: [CallbackQueryHandler(_extra_choice, pattern=r'^ext_(yes|no)$')],
        EXTRA_AMT: [MessageHandler(filters.TEXT & ~filters.COMMAND, _extra_amount)],
        REDUCTION: [CallbackQueryHandler(_reduction_choice, pattern=r'^red_(pay|term)$')],
        RESULTS: [
            CallbackQueryHandler(_save_loan, pattern=r'^save_loan$'),
            CallbackQueryHandler(_calc_cancel, pattern=r'^calc_cancel$'),
        ],
    },
    fallbacks=[MessageHandler(filters.Regex(r'^/(cancel|start)$'), _cancel_conversation)],
    name='calculator',
    persistent=False,
)
