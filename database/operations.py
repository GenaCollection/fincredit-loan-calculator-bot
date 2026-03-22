"""Synchronous helpers for loan and user operations."""

from database.database import get_session
from database.models import User, Loan


def get_user_loans(telegram_id: int):
    session = get_session()
    try:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        if not user:
            return []
        return (
            session.query(Loan)
            .filter_by(user_id=user.id)
            .order_by(Loan.id.desc())
            .all()
        )
    finally:
        session.close()


def get_loan_by_id(loan_id: int):
    session = get_session()
    try:
        return session.query(Loan).filter_by(id=loan_id).first()
    finally:
        session.close()


def get_loan_for_user(telegram_id: int, loan_id: int):
    """Кредит только если он принадлежит пользователю с данным telegram_id."""
    session = get_session()
    try:
        return (
            session.query(Loan)
            .join(User, Loan.user_id == User.id)
            .filter(User.telegram_id == telegram_id, Loan.id == loan_id)
            .first()
        )
    finally:
        session.close()


def delete_loan(telegram_id: int, loan_id: int) -> bool:
    session = get_session()
    try:
        loan = (
            session.query(Loan)
            .join(User, Loan.user_id == User.id)
            .filter(User.telegram_id == telegram_id, Loan.id == loan_id)
            .first()
        )
        if not loan:
            return False
        session.delete(loan)
        session.commit()
        return True
    except Exception:
        session.rollback()
        return False
    finally:
        session.close()


def save_loan_to_db(
    user_id: int,
    name: str,
    principal: float,
    annual_rate: float,
    months: int,
    payment_type: str,
    insurance: float = 0.0,
    extra_type: str | None = None,
    extra_amount: float = 0.0,
    reduction_type: str | None = None,
):
    """Создать и сохранить новый Loan, привязанный к пользователю по telegram_id."""
    session = get_session()
    try:
        user = session.query(User).filter_by(telegram_id=user_id).first()
        if not user:
            user = User(telegram_id=user_id, language="ru")
            session.add(user)
            session.commit()
            session.refresh(user)

        loan = Loan(
            user_id=user.id,
            name=name,
            principal=principal,
            annual_rate=annual_rate,
            months=months,
            payment_type=payment_type,
            insurance=insurance,
            extra_type=extra_type,
            extra_amount=extra_amount,
            reduction_type=reduction_type,
        )

        session.add(loan)
        session.commit()
        return loan
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
