from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Dict, Any, List

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from localization import get_text, get_user_language
from database.operations import save_loan_to_db
from utils.calculations import (
    calculate_annuity_schedule,
    calculate_differentiated_schedule,
)

logger = logging.getLogger(__name__)

# Состояния ConversationHandler
(
    AMOUNT,
    RATE,
    TERM,
    PAYMENT_TYPE,
    INSURANCE_YN,
    INSURANCE_AMOUNT,
    EXTRA_YN,
    EXTRA_TYPE,
    EXTRA_AMOUNT,
    EXTRA_REDUCTION_TYPE,
    CONFIRM_SAVE,
) = range(11)


@dataclass
class LoanDraft:
    amount: float | None = None
    rate: float | None = None
    term: int | None = None
    payment_type: str | None = None  # "annuity" / "diff"
    insurance: float = 0.0
    extra_type: str | None = None  # "once" / "period" / "recurring"
    extra_amount: float = 0.0
    reduction_type: str | None = None  # "payment" / "term"


def _get_draft(context: ContextTypes.DEFAULT_TYPE) -> LoanDraft:
    if "loan_draft" not in context.user_data:
        context.user_data["loan_draft"] = LoanDraft()
    return context.user_data["loan_draft"]


def _parse_float(value: str) -> float:
    return float(value.replace(" ", "").replace(",", "."))


def _parse_int(value: str) -> int:
    return int(value.replace(" ", ""))


# === Entry points ===


async def _entry_new_calc_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Старт калькулятора из reply-клавиатуры или из main_menu_callback_router."""
    user_id = update.effective_user.id
    lang = get_user_language(user_id)

    context.user_data["loan_draft"] = LoanDraft()

    await update.message.reply_text(
        get_text(lang, "calc_start"),
        parse_mode="Markdown",
    )
    return AMOUNT


# === Шаги диалога ===


async def _amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_user_language(user_id)

    raw = update.message.text.strip()
    try:
        amount = _parse_float(raw)
        if amount <= 0:
            raise ValueError()
    except ValueError:
        await update.message.reply_text(get_text(lang, "error_invalid_amount"))
        return AMOUNT

    draft = _get_draft(context)
    draft.amount = amount

    await update.message.reply_text(
        get_text(lang, "calc_amount_set", amount=amount),
        parse_mode="Markdown",
    )
    await update.message.reply_text(
        get_text(lang, "calc_rate_prompt"),
        parse_mode="Markdown",
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
        await update.message.reply_text(get_text(lang, "error_invalid_rate"))
        return RATE

    draft = _get_draft(context)
    draft.rate = rate

    await update.message.reply_text(
        get_text(lang, "calc_rate_set", rate=rate),
        parse_mode="Markdown",
    )
    await update.message.reply_text(
        get_text(lang, "calc_term_prompt"),
        parse_mode="Markdown",
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
        await update.message.reply_text(get_text(lang, "error_invalid_term"))
        return TERM

    draft = _get_draft(context)
    draft.term = months

    keyboard = [
        [
            InlineKeyboardButton(
                get_text(lang, "btn_annuity"), callback_data="type_annuity"
            ),
            InlineKeyboardButton(
                get_text(lang, "btn_differentiated"), callback_data="type_diff"
            ),
        ],
    ]

    await update.message.reply_text(
        get_text(lang, "calc_term_set", months=months),
        parse_mode="Markdown",
    )
    await update.message.reply_text(
        get_text(lang, "calc_payment_type"),
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown",
    )

    return PAYMENT_TYPE


async def _payment_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    lang = get_user_language(user_id)

    data = query.data
    draft = _get_draft(context)

    if data == "type_annuity":
        draft.payment_type = "annuity"
        info = get_text(lang, "annuity_info")
    else:
        draft.payment_type = "diff"
        info = get_text(lang, "diff_info")

    await query.edit_message_text(
        get_text(lang, "calc_payment_type") + "\n\n" + info,
        parse_mode="Markdown",
    )

    # Вопрос про страховку
    keyboard = [
        [
            InlineKeyboardButton(
                get_text(lang, "btn_insurance_yes"), callback_data="ins_yes"
            ),
            InlineKeyboardButton(
                get_text(lang, "btn_insurance_no"), callback_data="ins_no"
            ),
        ]
    ]

    await query.message.reply_text(
        get_text(lang, "calc_insurance"),
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown",
    )

    return INSURANCE_YN


async def _insurance_yn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    data = query.data

    draft = _get_draft(context)

    if data == "ins_no":
        draft.insurance = 0.0
        # Переходим сразу к вопросу о досрочном погашении
        keyboard = [
            [
                InlineKeyboardButton(
                    get_text(lang, "btn_extra_yes"), callback_data="extra_yes"
                ),
                InlineKeyboardButton(
                    get_text(lang, "btn_extra_no"), callback_data="extra_no"
                ),
            ]
        ]
        await query.edit_message_text(
            get_text(lang, "calc_extra_payments"),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )
        return EXTRA_YN

    # Если страхование есть — спрашиваем сумму
    await query.edit_message_text(
        get_text(lang, "calc_insurance_amount"),
        parse_mode="Markdown",
    )
    return INSURANCE_AMOUNT


async def _insurance_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_user_language(user_id)

    raw = update.message.text.strip()
    try:
        ins = _parse_float(raw)
        if ins < 0:
            raise ValueError()
    except ValueError:
        await update.message.reply_text(get_text(lang, "error_invalid_number"))
        return INSURANCE_AMOUNT

    draft = _get_draft(context)
    draft.insurance = ins

    await update.message.reply_text(
        get_text(lang, "results_insurance", insurance=ins),
        parse_mode="Markdown",
    )

    keyboard = [
        [
            InlineKeyboardButton(
                get_text(lang, "btn_extra_yes"), callback_data="extra_yes"
            ),
            InlineKeyboardButton(
                get_text(lang, "btn_extra_no"), callback_data="extra_no"
            ),
        ]
    ]

    await update.message.reply_text(
        get_text(lang, "calc_extra_payments"),
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown",
    )

    return EXTRA_YN


async def _extra_yn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    lang = get_user_language(user_id)

    data = query.data

    draft = _get_draft(context)

    if data == "extra_no":
        draft.extra_type = None
        draft.extra_amount = 0.0
        draft.reduction_type = None
        return await _calculate_and_show_results(query, context)

    # Если да — спрашиваем тип досрочного
    keyboard = [
        [
            InlineKeyboardButton(
                get_text(lang, "btn_extra_once"), callback_data="extra_once"
            ),
        ],
        [
            InlineKeyboardButton(
                get_text(lang, "btn_extra_period"), callback_data="extra_period"
            ),
        ],
        [
            InlineKeyboardButton(
                get_text(lang, "btn_extra_recurring"), callback_data="extra_recurring"
            ),
        ],
    ]

    await query.edit_message_text(
        get_text(lang, "calc_extra_type"),
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown",
    )

    return EXTRA_TYPE


async def _extra_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    lang = get_user_language(user_id)

    data = query.data
    draft = _get_draft(context)

    if data == "extra_once":
        draft.extra_type = "once"
        prompt_key = "calc_extra_amount"
    elif data == "extra_period":
        draft.extra_type = "period"
        prompt_key = "calc_extra_amount"
    else:
        draft.extra_type = "recurring"
        prompt_key = "calc_extra_monthly"

    await query.edit_message_text(
        get_text(lang, prompt_key),
        parse_mode="Markdown",
    )

    return EXTRA_AMOUNT


async def _extra_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_user_language(user_id)

    raw = update.message.text.strip()
    try:
        extra = _parse_float(raw)
        if extra <= 0:
            raise ValueError()
    except ValueError:
        await update.message.reply_text(get_text(lang, "error_invalid_number"))
        return EXTRA_AMOUNT

    draft = _get_draft(context)
    draft.extra_amount = extra

    keyboard = [
        [
            InlineKeyboardButton(
                get_text(lang, "btn_reduce_payment"), callback_data="reduce_payment"
            ),
        ],
        [
            InlineKeyboardButton(
                get_text(lang, "btn_reduce_term"), callback_data="reduce_term"
            ),
        ],
    ]

    await update.message.reply_text(
        get_text(lang, "calc_reduction_type"),
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown",
    )

    return EXTRA_REDUCTION_TYPE


async def _extra_reduction_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    lang = get_user_language(user_id)

    draft = _get_draft(context)
    data = query.data

    if data == "reduce_payment":
        draft.reduction_type = "payment"
    else:
        draft.reduction_type = "term"

    return await _calculate_and_show_results(query, context)


# === Расчёт и результат ===


async def _calculate_and_show_results(
    query_or_update, context: ContextTypes.DEFAULT_TYPE
):
    """Общий расчёт и показ результатов."""
    if hasattr(query_or_update, "callback_query"):
        query = query_or_update.callback_query
        await query.answer()
        message = query.message
        user_id = query_or_update.effective_user.id
    else:
        message = query_or_update.message
        user_id = query_or_update.effective_user.id

    lang = get_user_language(user_id)
    draft = _get_draft(context)

    if not (draft.amount and draft.rate is not None and draft.term and draft.payment_type):
        await message.reply_text(get_text(lang, "error_generic"))
        return ConversationHandler.END

    principal = draft.amount
    rate = draft.rate
    months = draft.term

    if draft.payment_type == "annuity":
        schedule = calculate_annuity_schedule(
            principal=principal,
            annual_rate=rate,
            months=months,
            insurance=draft.insurance,
            extra_amount=draft.extra_amount,
            extra_type=draft.extra_type,
            reduction_type=draft.reduction_type,
        )
        payment_type_str = get_text(lang, "payment_annuity")
    else:
        schedule = calculate_differentiated_schedule(
            principal=principal,
            annual_rate=rate,
            months=months,
            insurance=draft.insurance,
            extra_amount=draft.extra_amount,
            extra_type=draft.extra_type,
            reduction_type=draft.reduction_type,
        )
        payment_type_str = get_text(lang, "payment_differentiated")

    total_payment = sum(p.payment for p in schedule)
    overpayment = total_payment - principal
    actual_months = len(schedule)

    text_lines: List[str] = []

    text_lines.append(get_text(lang, "results_title"))

    text_lines.append(
        get_text(
            lang,
            "results_loan_info",
            principal=principal,
            rate=rate,
            months=months,
            payment_type=payment_type_str,
        )
    )

    if draft.insurance > 0:
        text_lines.append(
            get_text(lang, "results_insurance", insurance=draft.insurance)
        )

    if draft.extra_amount > 0 and draft.reduction_type:
        reduction_str = (
            get_text(lang, "reduction_payment")
            if draft.reduction_type == "payment"
            else get_text(lang, "reduction_term")
        )
        text_lines.append(
            get_text(
                lang,
                "results_extra",
                extra=draft.extra_amount,
                reduction=reduction_str,
            )
        )

    text_lines.append(get_text(lang, "results_summary"))

    text_lines.append(
        get_text(lang, "results_monthly", payment=schedule[0].payment)
    )
    text_lines.append(
        get_text(lang, "results_total", total=total_payment)
    )
    text_lines.append(
        get_text(lang, "results_overpayment", overpayment=overpayment)
    )
    text_lines.append(
        get_text(lang, "results_actual_months", months=actual_months)
    )

    if actual_months < months:
        saved_months = months - actual_months
        text_lines.append(
            get_text(lang, "results_saved_months", saved=saved_months)
        )

    text = "\n\n".join(text_lines)

    keyboard = [
        [
            InlineKeyboardButton(
                get_text(lang, "btn_save_loan"), callback_data="save_loan"
            )
        ],
        [
            InlineKeyboardButton(
                get_text(lang, "btn_back"),
                callback_data="main_menu:open",
            )
        ],
    ]

    await message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown",
    )

    return CONFIRM_SAVE


async def _confirm_save(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    data = query.data

    if data != "save_loan":
        await query.edit_message_text(
            get_text(lang, "add_payment_cancelled"),
            parse_mode="Markdown",
        )
        return ConversationHandler.END

    draft = _get_draft(context)

    loan_name = get_text(lang, "loan_name_template")

    save_loan_to_db(
        user_id=user_id,
        name=loan_name,
        principal=draft.amount,
        annual_rate=draft.rate,
        months=draft.term,
        payment_type=draft.payment_type,
        insurance=draft.insurance,
        extra_type=draft.extra_type,
        extra_amount=draft.extra_amount,
        reduction_type=draft.reduction_type,
    )

    await query.edit_message_text(
        get_text(lang, "loan_saved", name=loan_name, amount=draft.amount),
        parse_mode="Markdown",
    )

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    await update.message.reply_text(
        get_text(lang, "add_payment_cancelled"),
        parse_mode="Markdown",
    )
    return ConversationHandler.END


class NewCalcReplyFilter(filters.MessageFilter):
    def filter(self, message) -> bool:
        user_id = message.from_user.id
        lang = get_user_language(user_id)
        return message.text == get_text(lang, "btn_new_calc")


calculator_handler = ConversationHandler(
    entry_points=[
        MessageHandler(
            NewCalcReplyFilter() & filters.TEXT & ~filters.COMMAND,
            _entry_new_calc_reply,
        ),
    ],
    states={
        AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, _amount)],
        RATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, _rate)],
        TERM: [MessageHandler(filters.TEXT & ~filters.COMMAND, _term)],
        PAYMENT_TYPE: [
            CallbackQueryHandler(
                _payment_type,
                pattern=r"^type_(annuity|diff)$",
            )
        ],
        INSURANCE_YN: [
            CallbackQueryHandler(
                _insurance_yn,
                pattern=r"^ins_(yes|no)$",
            )
        ],
        INSURANCE_AMOUNT: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, _insurance_amount)
        ],
        EXTRA_YN: [
            CallbackQueryHandler(
                _extra_yn,
                pattern=r"^extra_(yes|no)$",
            )
        ],
        EXTRA_TYPE: [
            CallbackQueryHandler(
                _extra_type,
                pattern=r"^extra_(once|period|recurring)$",
            )
        ],
        EXTRA_AMOUNT: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, _extra_amount)
        ],
        EXTRA_REDUCTION_TYPE: [
            CallbackQueryHandler(
                _extra_reduction_type,
                pattern=r"^reduce_(payment|term)$",
            )
        ],
        CONFIRM_SAVE: [
            CallbackQueryHandler(
                _confirm_save,
                pattern=r"^(save_loan|main_menu:open)$",
            )
        ],
    },
    fallbacks=[MessageHandler(filters.COMMAND, cancel)],
    name="calculator_conversation",
    persistent=False,
)
