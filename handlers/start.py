from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)
from telegram.ext import ContextTypes
from telegram.error import BadRequest
import logging

from database import get_user_loans, get_loan_for_user, delete_loan
from localization import get_text, get_user_language

from callbacks import CallbackType, make_callback_data

logger = logging.getLogger(__name__)


def get_main_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                get_text(lang, "btn_new_calc"),
                callback_data=make_callback_data(CallbackType.MAIN_MENU, "new_calc"),
            )
        ],
        [
            InlineKeyboardButton(
                get_text(lang, "btn_my_loans"),
                callback_data=make_callback_data(CallbackType.MAIN_MENU, "my_loans"),
            )
        ],
        [
            InlineKeyboardButton(
                get_text(lang, "btn_help"),
                callback_data=make_callback_data(CallbackType.HELP, "open"),
            ),
            InlineKeyboardButton(
                get_text(lang, "btn_settings"),
                callback_data=make_callback_data(CallbackType.SETTINGS, "open"),
            ),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_reply_keyboard(lang: str) -> ReplyKeyboardMarkup:
    keyboard = [
        [get_text(lang, "btn_new_calc"), get_text(lang, "btn_my_loans")],
        [get_text(lang, "btn_help"), get_text(lang, "btn_settings")],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Стартовое приветствие и главное меню (и /start, и кнопка)."""
    user_id = update.effective_user.id
    lang = get_user_language(user_id)

    text_welcome = get_text(lang, "welcome")
    text_menu = get_text(lang, "main_menu")

    reply_kb = get_reply_keyboard(lang)
    inline_kb = get_main_menu_keyboard(lang)

    if update.callback_query:
        query = update.callback_query
        try:
            await query.answer()
            await query.edit_message_text(text_welcome, parse_mode="Markdown")
            await query.message.reply_text(
                text_menu,
                reply_markup=inline_kb,
                parse_mode="Markdown",
            )
        except BadRequest as e:
            logger.warning("BadRequest in start_command: %s", e)
            await query.message.reply_text(
                text_welcome,
                reply_markup=reply_kb,
                parse_mode="Markdown",
            )
            await query.message.reply_text(
                text_menu,
                reply_markup=inline_kb,
                parse_mode="Markdown",
            )
    else:
        await update.message.reply_text(
            text_welcome,
            reply_markup=reply_kb,
            parse_mode="Markdown",
        )
        await update.message.reply_text(
            text_menu,
            reply_markup=inline_kb,
            parse_mode="Markdown",
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    text = get_text(lang, "help_text")

    back_button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    get_text(lang, "btn_back"),
                    callback_data=make_callback_data(CallbackType.MAIN_MENU, "open"),
                )
            ]
        ]
    )

    if update.callback_query:
        query = update.callback_query
        try:
            await query.answer()
            await query.edit_message_text(
                text,
                reply_markup=back_button,
                parse_mode="Markdown",
            )
        except BadRequest as e:
            logger.warning("BadRequest in help_command: %s", e)
    else:
        await update.message.reply_text(text, parse_mode="Markdown")


async def myloans_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_my_loans(update, context)


async def show_my_loans(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_user_language(user_id)

    loans = get_user_loans(user_id)

    if not loans:
        text = get_text(lang, "my_loans_empty")
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        get_text(lang, "btn_back"),
                        callback_data=make_callback_data(CallbackType.MAIN_MENU, "open"),
                    )
                ]
            ]
        )
    else:
        text = get_text(lang, "my_loans_title")
        keyboard = []
        for loan in loans:
            keyboard.append(
                [
                    InlineKeyboardButton(
                        f"📝 {loan.name}",
                        callback_data=make_callback_data(
                            CallbackType.LOAN_DETAILS, str(loan.id)
                        ),
                    )
                ]
            )
        keyboard.append(
            [
                InlineKeyboardButton(
                    get_text(lang, "btn_back"),
                    callback_data=make_callback_data(CallbackType.MAIN_MENU, "open"),
                )
            ]
        )
        reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        if update.callback_query:
            await update.callback_query.edit_message_text(
                text,
                reply_markup=reply_markup,
                parse_mode="Markdown",
            )
        else:
            await update.message.reply_text(
                text,
                reply_markup=reply_markup,
                parse_mode="Markdown",
            )
    except BadRequest as e:
        logger.warning("BadRequest in show_my_loans: %s", e)


async def show_loan_details(
    update: Update, context: ContextTypes.DEFAULT_TYPE, loan_id: int
):
    user_id = update.effective_user.id
    lang = get_user_language(user_id)

    loan = get_loan_for_user(user_id, loan_id)
    if not loan:
        return

    text = get_text(lang, "loan_item").format(
        name=loan.name,
        amount=loan.principal,
        rate=loan.annual_rate,
        months=loan.months,
        payment=loan.monthly_payment or 0,
    )
    text += "\n\n" + get_text(lang, "loan_menu_title")

    keyboard = [
        [
            InlineKeyboardButton(
                get_text(lang, "btn_loan_schedule"),
                callback_data=make_callback_data(
                    CallbackType.LOAN_SCHEDULE, str(loan.id), "1"
                ),
            )
        ],
        [
            InlineKeyboardButton(
                get_text(lang, "btn_loan_add_payment"),
                callback_data=make_callback_data(
                    CallbackType.ADD_PAYMENT, str(loan.id)
                ),
            )
        ],
        [
            InlineKeyboardButton(
                get_text(lang, "btn_edit"),
                callback_data=f"edit_loan_{loan.id}",
            )
        ],
        [
            InlineKeyboardButton(
                get_text(lang, "btn_delete"),
                callback_data=f"delete_loan_{loan.id}",
            )
        ],
        [
            InlineKeyboardButton(
                get_text(lang, "btn_loan_back_list"),
                callback_data=make_callback_data(
                    CallbackType.MAIN_MENU, "my_loans"
                ),
            )
        ],
    ]

    try:
        await update.callback_query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )
    except BadRequest as e:
        logger.warning("BadRequest in show_loan_details: %s", e)


async def route_text_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reply-клавиатура и другие текстовые сообщения."""
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    text = (update.message.text or "").strip()

    if text == get_text(lang, "btn_my_loans"):
        await show_my_loans(update, context)
        return

    if text == get_text(lang, "btn_settings"):
        from handlers.settings import settings_command

        await settings_command(update, context)
        return

    if text == get_text(lang, "btn_help"):
        await help_command(update, context)
        return

    if text == get_text(lang, "btn_new_calc"):
        from handlers.calculator import _entry_new_calc_reply

        await _entry_new_calc_reply(update, context)
        return
