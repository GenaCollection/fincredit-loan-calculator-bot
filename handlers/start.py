"""Start command handlers with localization support"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, filters
from database import get_session
from database.models import User, Loan, PaymentType, ExtraPayment, ExtraPaymentType
from localization import get_text  # ← ВОТ ГДЕ ИСПОЛЬЗУЕТСЯ!
from utils.calculations import calculate_loan_totals, calculate_annuity_schedule_with_extras
import logging

logger = logging.getLogger(__name__)

def _format_money(value: float) -> str:
    try:
        return f"{value:,.0f}".replace(",", " ")
    except Exception:
        return str(value)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    session = get_session()
    
    try:
        # Check if user exists in database
        db_user = session.query(User).filter_by(telegram_id=user.id).first()
        if not db_user:
            # Create new user with default language (Russian)
            db_user = User(
                telegram_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                language='ru'  # По умолчанию русский
            )
            session.add(db_user)
            session.commit()
        
        # Получаем текст приветствия НА ЯЗЫКЕ ПОЛЬЗОВАТЕЛЯ
        welcome_text = get_text(user.id, 'welcome')
        
        # Получаем тексты кнопок НА ЯЗЫКЕ ПОЛЬЗОВАТЕЛЯ
        keyboard = [
            [InlineKeyboardButton(
                get_text(user.id, 'btn_new_calc'), 
                callback_data="new_calc"
            )],
            [InlineKeyboardButton(
                get_text(user.id, 'btn_my_loans'), 
                callback_data="my_loans"
            )],
            [InlineKeyboardButton(
                get_text(user.id, 'btn_help'), 
                callback_data="help"
            ),
             InlineKeyboardButton(
                get_text(user.id, 'btn_settings'), 
                callback_data="settings"
            )]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    finally:
        session.close()


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    user = update.effective_user
    
    # Получаем текст справки НА ЯЗЫКЕ ПОЛЬЗОВАТЕЛЯ
    help_text = get_text(user.id, 'help_text')
    
    await update.message.reply_text(help_text, parse_mode='Markdown')


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    
    if query.data == "back_to_menu":
        # Показываем главное меню
        welcome_text = get_text(user.id, 'main_menu') + '\n\n' + get_text(user.id, 'welcome')
        
        keyboard = [
            [InlineKeyboardButton(
                get_text(user.id, 'btn_new_calc'), 
                callback_data="new_calc"
            )],
            [InlineKeyboardButton(
                get_text(user.id, 'btn_my_loans'), 
                callback_data="my_loans"
            )],
            [InlineKeyboardButton(
                get_text(user.id, 'btn_help'), 
                callback_data="help"
            ),
             InlineKeyboardButton(
                get_text(user.id, 'btn_settings'), 
                callback_data="settings"
            )]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            welcome_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    elif query.data == "help":
        help_text = get_text(user.id, 'help_text')
        
        await query.edit_message_text(
            help_text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    get_text(user.id, 'btn_back'), 
                    callback_data="back_to_menu"
                )
            ]])
        )
    
    elif query.data == "my_loans":
        session = get_session()
        try:
            db_user = session.query(User).filter_by(telegram_id=user.id).first()
            if not db_user:
                my_loans_text = get_text(user.id, 'my_loans_title') + get_text(user.id, 'my_loans_empty')
                await query.edit_message_text(
                    my_loans_text,
                    parse_mode='Markdown',
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton(get_text(user.id, 'btn_back'), callback_data="back_to_menu")
                    ]])
                )
                return

            loans = (
                session.query(Loan)
                .filter_by(user_id=db_user.id, is_active=True)
                .order_by(Loan.created_at.desc())
                .all()
            )

            if not loans:
                my_loans_text = get_text(user.id, 'my_loans_title') + get_text(user.id, 'my_loans_empty')
                await query.edit_message_text(
                    my_loans_text,
                    parse_mode='Markdown',
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton(get_text(user.id, 'btn_back'), callback_data="back_to_menu")
                    ]])
                )
                return

            text = get_text(user.id, 'my_loans_title')
            keyboard = []

            for idx, loan in enumerate(loans[:20], start=1):
                if loan.monthly_payment is not None:
                    monthly_payment = loan.monthly_payment
                else:
                    ptype = 'annuity' if loan.payment_type == PaymentType.ANNUITY else 'differentiated'
                    totals = calculate_loan_totals(loan.principal, loan.annual_rate, loan.months, ptype)
                    monthly_payment = totals['monthly_payment']
                    if loan.insurance_monthly:
                        monthly_payment += loan.insurance_monthly

                text += (
                    f"{idx}) *{loan.name}* — {_format_money(loan.principal)} ₽ — "
                    f"{_format_money(monthly_payment)} ₽/мес\n"
                )
                keyboard.append([InlineKeyboardButton(f"{idx}. {loan.name}", callback_data=f"loan_{loan.id}")])

            keyboard.append([InlineKeyboardButton(get_text(user.id, 'btn_back'), callback_data="back_to_menu")])

            await query.edit_message_text(
                text,
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        finally:
            session.close()


async def handle_add_payment_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user messages during 'add payment' flow (amount -> month)."""
    user = update.effective_user
    state = context.user_data.get('add_payment_state')
    loan_id = context.user_data.get('add_payment_loan_id')
    if not state or not loan_id:
        return  # not in flow

    text = update.message.text.strip()

    if state == 'amount':
        try:
            amount = float(text.replace(' ', '').replace(',', '.'))
            if amount <= 0:
                await update.message.reply_text(get_text(user.id, 'error_invalid_number'))
                return
        except ValueError:
            await update.message.reply_text(get_text(user.id, 'error_invalid_number'))
            return

        context.user_data['add_payment_amount'] = amount
        context.user_data['add_payment_state'] = 'month'
        await update.message.reply_text(get_text(user.id, 'add_payment_prompt_month'))
        return

    if state == 'month':
        try:
            month = int(text)
            if month <= 0 or month > 1200:
                await update.message.reply_text(get_text(user.id, 'error_invalid_number'))
                return
        except ValueError:
            await update.message.reply_text(get_text(user.id, 'error_invalid_number'))
            return

        amount = float(context.user_data.get('add_payment_amount', 0.0) or 0.0)

        session = get_session()
        try:
            db_user = session.query(User).filter_by(telegram_id=user.id).first()
            loan = session.query(Loan).filter_by(id=loan_id, user_id=db_user.id, is_active=True).first() if db_user else None
            if not loan:
                await update.message.reply_text(get_text(user.id, 'error_generic'))
                return

            ep = ExtraPayment(
                loan_id=loan.id,
                amount=amount,
                payment_month=month,
                extra_type=ExtraPaymentType.ONE_TIME,
            )
            session.add(ep)

            # Recalculate schedule and cached totals
            extras = []
            for e in loan.extra_payments + [ep]:
                extras.append({'month': e.payment_month, 'amount': e.amount, 'type': e.extra_type.value})

            schedule, summary = calculate_annuity_schedule_with_extras(
                principal=loan.principal,
                annual_rate=loan.annual_rate,
                months=loan.months,
                start_date=loan.start_date,
                extra_payments=extras,
                reduction_type=loan.reduction_type.value if loan.reduction_type else 'term',
                insurance_monthly=loan.insurance_monthly or 0.0,
                use_exact_days=loan.use_exact_days,
            )

            loan.has_extra_payments = True
            loan.extra_payment_amount = amount
            loan.extra_payment_type = ExtraPaymentType.RECURRING if loan.extra_payment_type == ExtraPaymentType.RECURRING else ExtraPaymentType.ONE_TIME
            if schedule:
                loan.monthly_payment = schedule[0]['payment_amount']
            loan.total_payment = summary['total_payment']
            loan.total_overpayment = summary['overpayment']
            loan.actual_months = summary['actual_months']

            session.commit()

            await update.message.reply_text(
                get_text(user.id, 'add_payment_saved', amount=amount, month=month),
                parse_mode='Markdown',
            )
        except Exception:
            session.rollback()
            await update.message.reply_text(get_text(user.id, 'error_generic'))
        finally:
            session.close()
            # clear state
            context.user_data.pop('add_payment_state', None)
            context.user_data.pop('add_payment_loan_id', None)
            context.user_data.pop('add_payment_amount', None)

    elif query.data.startswith("loan_schedule_"):
        # loan_schedule_<loan_id>_<page>
        _, _, loan_id_str, page_str = query.data.split("_", 3)
        try:
            loan_id = int(loan_id_str)
            page = int(page_str)
        except ValueError:
            await query.edit_message_text(get_text(user.id, 'error_generic'))
            return

        session = get_session()
        try:
            db_user = session.query(User).filter_by(telegram_id=user.id).first()
            if not db_user:
                await query.edit_message_text(get_text(user.id, 'error_generic'))
                return

            loan = (
                session.query(Loan)
                .filter_by(id=loan_id, user_id=db_user.id, is_active=True)
                .first()
            )
            if not loan:
                await query.edit_message_text(get_text(user.id, 'error_generic'))
                return

            # Build extra payments list from DB
            extras = []
            for ep in loan.extra_payments:
                extras.append({
                    'month': ep.payment_month,
                    'amount': ep.amount,
                    'type': ep.extra_type.value,
                })

            schedule, summary = calculate_annuity_schedule_with_extras(
                principal=loan.principal,
                annual_rate=loan.annual_rate,
                months=loan.months,
                start_date=loan.start_date,
                extra_payments=extras if extras else None,
                reduction_type=loan.reduction_type.value if loan.reduction_type else 'term',
                insurance_monthly=loan.insurance_monthly or 0.0,
                use_exact_days=loan.use_exact_days,
            )

            if not schedule:
                await query.edit_message_text(
                    get_text(user.id, 'schedule_empty'),
                    parse_mode='Markdown',
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton(get_text(user.id, 'btn_loan_back_list'), callback_data="my_loans")
                    ]])
                )
                return

            page_size = 10
            total_pages = (len(schedule) + page_size - 1) // page_size
            page = max(1, min(page, total_pages))
            start_idx = (page - 1) * page_size
            end_idx = start_idx + page_size

            lines = []
            lines.append(get_text(user.id, 'schedule_title', name=loan.name))
            lines.append(get_text(user.id, 'schedule_header'))
            for row in schedule[start_idx:end_idx]:
                lines.append(get_text(
                    user.id,
                    'schedule_row',
                    n=row['payment_number'],
                    date=row['payment_date'].strftime('%d.%m.%Y'),
                    payment=row['payment_amount'],
                    principal=row['principal'],
                    interest=row['interest'],
                    balance=row['remaining_balance'],
                ))
            lines.append(get_text(user.id, 'schedule_page_info', page=page, pages=total_pages))

            text = "".join(lines)

            nav_buttons = []
            if page > 1:
                nav_buttons.append(InlineKeyboardButton("⬅️", callback_data=f"loan_schedule_{loan.id}_{page-1}"))
            if page < total_pages:
                nav_buttons.append(InlineKeyboardButton("➡️", callback_data=f"loan_schedule_{loan.id}_{page+1}"))

            keyboard = []
            if nav_buttons:
                keyboard.append(nav_buttons)
            keyboard.append([InlineKeyboardButton(get_text(user.id, 'btn_loan_back_list'), callback_data="my_loans")])

            await query.edit_message_text(
                text,
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        finally:
            session.close()

    elif query.data.startswith("loan_addpay_"):
        # loan_addpay_<loan_id> — старт диалога добавления платежа
        _, _, loan_id_str = query.data.split("_", 2)
        try:
            loan_id = int(loan_id_str)
        except ValueError:
            await query.edit_message_text(get_text(user.id, 'error_generic'))
            return

        # сохраняем в user_data, какой кредит редактируем
        context.user_data['add_payment_loan_id'] = loan_id
        context.user_data['add_payment_state'] = 'amount'

        await query.edit_message_text(
            get_text(user.id, 'add_payment_prompt_amount'),
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(get_text(user.id, 'btn_back'), callback_data=f"loan_{loan_id}")
            ]])
        )

    elif query.data.startswith("loan_"):
        loan_id_str = query.data.replace("loan_", "", 1)
        try:
            loan_id = int(loan_id_str)
        except ValueError:
            await query.edit_message_text(get_text(user.id, 'error_generic'))
            return

        session = get_session()
        try:
            db_user = session.query(User).filter_by(telegram_id=user.id).first()
            if not db_user:
                await query.edit_message_text(get_text(user.id, 'error_generic'))
                return

            loan = (
                session.query(Loan)
                .filter_by(id=loan_id, user_id=db_user.id, is_active=True)
                .first()
            )
            if not loan:
                await query.edit_message_text(get_text(user.id, 'error_generic'))
                return

            if loan.monthly_payment is not None:
                monthly_payment = loan.monthly_payment
            else:
                ptype = 'annuity' if loan.payment_type == PaymentType.ANNUITY else 'differentiated'
                totals = calculate_loan_totals(loan.principal, loan.annual_rate, loan.months, ptype)
                monthly_payment = totals['monthly_payment']
                if loan.insurance_monthly:
                    monthly_payment += loan.insurance_monthly

            text = get_text(
                user.id,
                'loan_item',
                name=loan.name,
                amount=loan.principal,
                rate=loan.annual_rate,
                months=loan.months,
                payment=monthly_payment,
            )
            text += get_text(user.id, 'loan_menu_title')

            keyboard = [
                [
                    InlineKeyboardButton(get_text(user.id, 'btn_loan_schedule'), callback_data=f"loan_schedule_{loan.id}_1")
                ],
                [
                    InlineKeyboardButton(get_text(user.id, 'btn_loan_add_payment'), callback_data=f"loan_addpay_{loan.id}")
                ],
                [
                    InlineKeyboardButton(get_text(user.id, 'btn_loan_back_list'), callback_data="my_loans"),
                    InlineKeyboardButton(get_text(user.id, 'btn_back'), callback_data="back_to_menu"),
                ],
            ]

            await query.edit_message_text(
                text,
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        finally:
            session.close()
