"""Просмотр графика платежей с пагинацией."""
import logging
from datetime import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from database import get_session
from database.models import ExtraPayment
from database.operations import get_loan_for_user
from localization import get_text, get_user_language
from utils.loan_schedule import build_schedule_for_loan

logger = logging.getLogger(__name__)

ROWS_PER_PAGE = 7


def _fmt_date(dt: datetime) -> str:
    if hasattr(dt, "strftime"):
        return dt.strftime("%d.%m.%Y")
    return str(dt)


async def loan_schedule_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    parts = query.data.split("_")
    # loan_schedule_{id}_{page}
    try:
        loan_id = int(parts[2])
        page = max(1, int(parts[3]))
    except (IndexError, ValueError):
        return

    user_id = query.from_user.id
    lang = get_user_language(user_id)

    session = get_session()
    try:
        loan = get_loan_for_user(user_id, loan_id)
        if not loan:
            await query.edit_message_text(get_text(lang, "error_generic"))
            return

        extras = session.query(ExtraPayment).filter_by(loan_id=loan.id).all()
        schedule = build_schedule_for_loan(loan, extras)
    except Exception as e:
        logger.exception(e)
        await query.edit_message_text(get_text(lang, "error_generic"))
        return
    finally:
        session.close()

    if not schedule:
        await query.edit_message_text(
            get_text(lang, "schedule_empty"),
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(get_text(lang, "btn_back"), callback_data=f"view_loan_{loan_id}")]]
            ),
        )
        return

    total_pages = max(1, (len(schedule) + ROWS_PER_PAGE - 1) // ROWS_PER_PAGE)
    if page > total_pages:
        page = total_pages

    start_i = (page - 1) * ROWS_PER_PAGE
    chunk = schedule[start_i : start_i + ROWS_PER_PAGE]

    # Убираем * из локализованного заголовка — график без parse_mode, чтобы имя кредита не ломало разметку
    text = get_text(lang, "schedule_title", name=loan.name).replace("*", "")
    text += get_text(lang, "schedule_header")

    for row in chunk:
        n = row["payment_number"]
        dt = row.get("payment_date")
        text += get_text(
            lang,
            "schedule_row",
            n=n,
            date=_fmt_date(dt) if dt else "",
            payment=row["payment_amount"],
            principal=row["principal"],
            interest=row["interest"],
            balance=row["remaining_balance"],
        )

    text += get_text(lang, "schedule_page_info", page=page, pages=total_pages)

    nav_row = []
    if page > 1:
        nav_row.append(
            InlineKeyboardButton("◀️", callback_data=f"loan_schedule_{loan_id}_{page - 1}")
        )
    if page < total_pages:
        nav_row.append(
            InlineKeyboardButton("▶️", callback_data=f"loan_schedule_{loan_id}_{page + 1}")
        )
    keyboard = [nav_row] if nav_row else []
    keyboard.append(
        [InlineKeyboardButton(get_text(lang, "btn_back"), callback_data=f"view_loan_{loan_id}")]
    )

    try:
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    except telegram.error.BadRequest as e:
        logger.warning("schedule edit failed: %s", e)
